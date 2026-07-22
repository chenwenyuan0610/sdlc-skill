#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The encoding line and this guard are deliberately ASCII-only and come
# before everything else, so an old Python still parses this far and can
# print a readable message instead of a PEP-263 syntax error.
import sys
if sys.version_info < (3, 8):
    sys.stderr.write(
        "\nThis installer needs Python 3.8 or newer.\n"
        "  macOS / Linux:  python3 install.py\n"
        "  Windows:        py install.py\n\n")
    sys.exit(1)

"""SDLC skill pack installer.

Installs the 9 SDLC phase skills, the shared sdlc-orchestrator reference
directory and the 3 subagent role files either for the current user or for
one project, then writes the Entry Protocol into the matching instruction
file for Claude Code or Codex.

Standard library only. Works on macOS, Linux and Windows.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Optional, Tuple

# Decorative glyphs die on legacy Windows codepages once stdout is a file
# or a pipe, so make the stream forgiving before anything is printed.
for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        try:
            _reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

PACK = Path(__file__).resolve().parent

SKILLS = [
    "product-discovery",
    "requirement-scoping",
    "system-design",
    "dev-setup",
    "implementation-handoff",
    "qa-handoff",
    "release-handoff",
    "ops-feedback",
    "change-request",
]
ORCHESTRATOR = "sdlc-orchestrator"
AGENTS = ["sdlc-implementer.md", "sdlc-reviewer.md", "sdlc-verifier.md"]

BEGIN = "<!-- SDLC-ENTRY-PROTOCOL:BEGIN — managed by install.py, edits here are overwritten on reinstall -->"
END = "<!-- SDLC-ENTRY-PROTOCOL:END -->"

# Set once anything lands on disk, so an interrupt can report honestly.
WROTE_ANYTHING = False


# --------------------------------------------------------------------------
# terminal helpers
# --------------------------------------------------------------------------

def _encodable(text):
    enc = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        text.encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


FANCY = _encodable("✓ ✗ ⚠ ›")
TICK = "✓" if FANCY else "[OK]"
CROSS = "✗" if FANCY else "[X]"
WARN = "⚠" if FANCY else "[!]"
POINT = "›" if FANCY else ">"


def supports_colour():
    if os.environ.get("NO_COLOR"):
        return False
    if os.name == "nt" and not os.environ.get("WT_SESSION"):
        return False
    return sys.stdout.isatty()


_C = supports_colour()


def paint(text, code):
    return "\033[{}m{}\033[0m".format(code, text) if _C else text


def bold(t):
    return paint(t, "1")


def dim(t):
    return paint(t, "2")


def green(t):
    return paint(t, "32")


def yellow(t):
    return paint(t, "33")


def red(t):
    return paint(t, "31")


def heading(text):
    print("\n" + bold(text))
    print(dim("-" * max(len(text), 44)))


def ask_choice(question, options, default=1):
    """options: list of (label, description). Returns 1-based index."""
    print("\n" + bold(question))
    for i, (label, desc) in enumerate(options, 1):
        marker = green(POINT) if i == default else " "
        print("  {} {}. {}".format(marker, i, label))
        if desc:
            print("      " + dim(desc))
    while True:
        raw = input("\n選擇 [{}]: ".format(default)).strip()
        if not raw:
            return default
        try:
            value = int(raw)
        except ValueError:
            print(red("  請輸入 1-{} 之間的數字。".format(len(options))))
            continue
        if 1 <= value <= len(options):
            return value
        print(red("  請輸入 1-{} 之間的數字。".format(len(options))))


def clean_path_input(raw):
    """Normalise a path the user typed, pasted or dragged in.

    Terminals hand back very different text for the same folder: Windows
    "copy as path" wraps it in quotes, while macOS Terminal and iTerm
    backslash-escape every space when you drag a folder in.
    """
    raw = raw.strip().strip("'\"")
    if os.name != "nt":
        # Only unescape where the backslash is an escape character; on
        # Windows it is the path separator and must survive untouched.
        raw = raw.replace("\\ ", " ")
    return os.path.expanduser(os.path.expandvars(raw))


def ask_path(question, hint=None):
    while True:
        print("\n" + bold(question))
        if hint:
            print("  " + dim(hint))
        cleaned = clean_path_input(input("> "))
        if not cleaned:
            print(red("  路徑不能空白。"))
            continue
        # Keep the lexical path so a later safety check can still see
        # components such as .claude and symlinks. resolve() would erase
        # exactly the information needed to reject unsafe destinations.
        path = Path(os.path.abspath(cleaned))
        if path.exists() and not path.is_dir():
            print(red("  這是一個檔案，不是資料夾：{}".format(path)))
            continue
        if not path.is_dir():
            print(red("  找不到這個資料夾：{}".format(path)))
            print("  " + dim("常見原因：路徑打錯字，或複製時漏掉了一段。"))
            print(red("  {} 若堅持使用，會在這個位置建立一個全新的空資料夾——".format(WARN)))
            print(red("     那不是你現有的工作區，裝進去等於白裝。"))
            if input("  重新輸入請直接按 Enter（建議）；確定要建新資料夾請輸入 yes: ").strip().lower() != "yes":
                continue
        return path


def is_tool_config_directory(path: Path) -> bool:
    """Return whether path is a tool config directory or below one."""
    return any(
        part.casefold() in (".claude", ".codex", ".agents")
        for part in path.parts
    )


def normalized_project_root(path: Path) -> Path:
    """Validate lexical/resolved project paths and return the real root."""
    lexical = Path(os.path.abspath(str(path)))
    resolved = lexical.resolve()
    if is_tool_config_directory(lexical) or is_tool_config_directory(resolved):
        raise ValueError(
            "project_root must not be .claude, .codex or .agents, "
            "including through a symbolic link")
    return resolved


def ask_project_root() -> Path:
    """Ask for a project root, rejecting tool config directories."""
    while True:
        root = ask_path(
            "你的專案／工作區根目錄在哪裡？",
            "請選平常用 Claude Code / Codex 開啟的那一層；不要選裡面的 .claude、.codex 或 .agents。")
        try:
            return normalized_project_root(root)
        except ValueError:
            pass
        print(red("  你選到工具設定資料夾或它的子資料夾：{}".format(root)))
        print(red("  請改選專案／工作區根目錄，否則會產生重複的設定目錄。"))
        print("  " + dim("請選不含 .claude / .codex / .agents 的專案根目錄。"))


def codex_home_path(home: Optional[Path] = None,
                    environ: Optional[Mapping[str, str]] = None) -> Path:
    """Return an absolute lexical CODEX_HOME, defaulting to ~/.codex."""
    user_home = Path.home() if home is None else Path(home)
    env = os.environ if environ is None else environ
    configured = env.get("CODEX_HOME")
    if configured:
        return Path(os.path.abspath(clean_path_input(configured)))
    return user_home / ".codex"


def entry_file_locations(
        scope: str,
        project_root: Optional[Path] = None,
        home: Optional[Path] = None,
        environ: Optional[Mapping[str, str]] = None,
) -> List[Path]:
    """Return the Claude Code and Codex entry-file targets."""
    user_home = Path.home() if home is None else Path(home)
    if scope == "personal":
        return [
            user_home / ".claude" / "CLAUDE.md",
            codex_home_path(user_home, environ) / "AGENTS.md",
        ]
    if scope == "project":
        if project_root is None:
            raise ValueError("project_root is required for project scope")
        root = normalized_project_root(project_root)
        return [root / "CLAUDE.md", root / "AGENTS.md"]
    raise ValueError("scope must be 'personal' or 'project'")


def standard_storage_root(
        scope: str,
        platform: str,
        kind: str,
        project_root: Optional[Path] = None,
        home: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """Return one standard storage root and its safety boundary."""
    user_home = Path.home() if home is None else Path(home)
    if scope == "personal":
        boundary = user_home
    elif scope == "project":
        if project_root is None:
            raise ValueError("project_root is required for project scope")
        boundary = normalized_project_root(project_root)
    else:
        raise ValueError("scope must be 'personal' or 'project'")

    if kind not in ("skills", "agents"):
        raise ValueError("kind must be 'skills' or 'agents'")
    if platform == "claude":
        base = boundary / ".claude"
    elif platform == "codex":
        base = boundary / ".agents"
    else:
        raise ValueError("platform must be 'claude' or 'codex'")
    return base / kind, boundary


def choose_storage_root(
        kind: str,
        scope: str,
        entry_platform: str,
        project_root: Optional[Path],
) -> Tuple[Path, Path, str]:
    """Ask for one payload root, offering two standards and an exact path."""
    if kind not in ("skills", "agents"):
        raise ValueError("kind must be 'skills' or 'agents'")
    other_platform = "codex" if entry_platform == "claude" else "claude"
    recommended = standard_storage_root(
        scope, entry_platform, kind, project_root)
    alternative = standard_storage_root(
        scope, other_platform, kind, project_root)
    names = {"claude": "Claude Code", "codex": "Codex"}
    labels = {"skills": ("skill", "skills"), "agents": ("角色檔", "agents")}
    label, directory_name = labels[kind]
    question = "skill 要放在哪裡？" if kind == "skills" else "角色檔要放在哪裡？"

    choice = ask_choice(
        question,
        [
            ("{} 標準位置（建議，與所選規則檔相符）".format(
                names[entry_platform]), str(recommended[0])),
            ("{} 標準位置".format(names[other_platform]),
             str(alternative[0])),
            ("依個人習慣指定其他位置",
             "需輸入本次安裝範圍內的完整絕對路徑（不可使用相對路徑）"),
        ],
        default=1,
    )
    if choice == 1:
        return recommended[0], recommended[1], entry_platform
    if choice == 2:
        return alternative[0], alternative[1], other_platform

    boundary = (Path.home().resolve() if scope == "personal"
                else normalized_project_root(project_root))
    custom = ask_path(
        "請輸入 {} 的完整絕對安裝路徑".format(label),
        "例如 /Users/name/project/.agents/{} 或 "
        "C:\\Users\\name\\project\\.agents\\{}；"
        "不要輸入 .agents/{} 這類相對路徑。不存在時會在安全檢查通過後建立。".format(
            directory_name, directory_name, directory_name))
    return _canonical_storage_input(custom), boundary, "custom"


def choose_install_scope() -> Tuple[str, Optional[Path]]:
    """Ask for personal versus project scope; only project needs a path."""
    home = Path.home()
    choice = ask_choice(
        "要安裝給誰使用？",
        [
            ("個人／全域安裝（這台電腦上的所有專案）",
             "下一步會依你選的工具，建議標準的 skill 位置"),
            ("單一專案／工作區",
             "skill 只放進你接下來選擇的專案，不影響其他專案"),
        ],
        default=1,
    )
    if choice == 1:
        return "personal", None
    return "project", ask_project_root()


class UnsafeDestinationError(Exception):
    """Raised when an install destination could escape its intended boundary."""


def _absolute_path(path: Path) -> Path:
    """Return an absolute lexical path without resolving symlinks."""
    return Path(os.path.abspath(str(path)))


def _is_relative_to(path: Path, boundary: Path) -> bool:
    """Python 3.8-compatible Path.is_relative_to()."""
    try:
        path.relative_to(boundary)
        return True
    except ValueError:
        return False


def _nearest_existing_ancestor(path: Path) -> Path:
    """Return path itself or its closest existing parent."""
    current = path
    while (not current.exists() and not current.is_symlink()
           and current.parent != current):
        current = current.parent
    return current


def _canonical_storage_input(path: Path) -> Path:
    """Resolve normal aliases while preserving broken symlinks for preflight."""
    lexical = _absolute_path(path)
    current = lexical
    while current.parent != current:
        if current.is_symlink() and not current.exists():
            return lexical
        current = current.parent
    return lexical.resolve()


def validate_destination(path: Path, boundary: Path, label: str) -> Path:
    """Validate containment and reject symlinks below the intended boundary."""
    target = _absolute_path(path)
    lexical_boundary = _absolute_path(boundary)
    if lexical_boundary.is_symlink():
        raise UnsafeDestinationError(
            "{} 的允許範圍是 symbolic link：{}".format(
                label, lexical_boundary))
    if lexical_boundary.exists() and not lexical_boundary.is_dir():
        raise UnsafeDestinationError(
            "{} 的允許範圍不是資料夾：{}".format(label, lexical_boundary))
    existing_ancestor = _nearest_existing_ancestor(lexical_boundary)
    if existing_ancestor.is_symlink():
        raise UnsafeDestinationError(
            "{} 的既有上層是 symbolic link：{}".format(
                label, existing_ancestor))
    if existing_ancestor.exists() and not existing_ancestor.is_dir():
        raise UnsafeDestinationError(
            "{} 的既有上層不是資料夾：{}".format(label, existing_ancestor))
    if not _is_relative_to(target, lexical_boundary):
        raise UnsafeDestinationError(
            "{} 不在允許的範圍內：{}（應位於 {}）".format(
                label, target, lexical_boundary))

    relative = target.relative_to(lexical_boundary)
    current = lexical_boundary
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise UnsafeDestinationError(
                "{} 含有 symbolic link：{}。請移除連結或改選安全的目錄。".format(
                    label, current))
        if current != target and current.exists() and not current.is_dir():
            raise UnsafeDestinationError(
                "{} 的上層路徑不是資料夾：{}".format(label, current))

    resolved_boundary = lexical_boundary.resolve()
    resolved_target = target.resolve()
    if not _is_relative_to(resolved_target, resolved_boundary):
        raise UnsafeDestinationError(
            "{} 解析後超出允許範圍：{}（應位於 {}）".format(
                label, resolved_target, resolved_boundary))
    return target


def _validate_directory_destination(path: Path, boundary: Path, label: str) -> Path:
    target = validate_destination(path, boundary, label)
    if target.exists() and not target.is_dir():
        raise UnsafeDestinationError("{} 必須是資料夾：{}".format(label, target))
    return target


def _validate_file_destination(path: Path, boundary: Path, label: str) -> Path:
    target = validate_destination(path, boundary, label)
    if target.exists() and not target.is_file():
        raise UnsafeDestinationError("{} 必須是一般檔案：{}".format(label, target))
    return target


def _contains_path(parent: Path, child: Path) -> bool:
    """Return whether parent contains child, treating equality as containment."""
    return _is_relative_to(_absolute_path(child), _absolute_path(parent))


def _reject_storage_root_shape(path: Path, boundary: Path, label: str) -> None:
    """Prevent payload files from being copied into an overly broad container."""
    target = _absolute_path(path)
    allowed = _absolute_path(boundary)
    if target == allowed:
        raise UnsafeDestinationError(
            "{} 不可直接使用本次安裝範圍根目錄：{}".format(label, target))
    if target.parent == allowed and target.name.casefold() in (
            ".claude", ".codex", ".agents"):
        raise UnsafeDestinationError(
            "{} 不可直接使用工具設定容器：{}。請選裡面的精確目錄。".format(
                label, target))


def _reject_overlapping_roots(
        skills_root: Path, agents_root: Path, attic: Path) -> None:
    """Reject roots whose copy/backup operations could consume one another."""
    pairs = (
        ("skill 目錄", skills_root, "角色目錄", agents_root),
        ("skill 目錄", skills_root, "skill 備份目錄", attic),
        ("角色目錄", agents_root, "skill 備份目錄", attic),
    )
    for left_label, left, right_label, right in pairs:
        if _contains_path(left, right) or _contains_path(right, left):
            raise UnsafeDestinationError(
                "{} 與 {} 不可相同或互相包含：{}；{}".format(
                    left_label, right_label, left, right))


def _reject_tree_symlinks(path: Path, label: str) -> None:
    """Reject symlinks already stored inside a package-owned directory."""
    if not path.is_dir():
        return

    def raise_walk_error(error):
        raise error

    for root, dirnames, filenames in os.walk(
            str(path), topdown=True, onerror=raise_walk_error, followlinks=False):
        for name in dirnames + filenames:
            candidate = Path(root) / name
            if candidate.is_symlink():
                raise UnsafeDestinationError(
                    "{} 內含 symbolic link：{}。請先移除或移出再安裝。".format(
                        label, candidate))


def preflight_installation(
        scope: str,
        project_root: Optional[Path],
        skills_root: Path,
        agents_root: Path,
        attic: Path,
        skills_boundary: Path,
        agents_boundary: Path,
        entry_file: Optional[Path],
        entry_files: List[Path],
) -> None:
    """Validate every selected destination before the installer writes anything."""
    if scope == "project" and project_root is None:
        raise UnsafeDestinationError("找不到安裝範圍的根目錄。")

    _reject_storage_root_shape(skills_root, skills_boundary, "skill 目錄")
    _reject_storage_root_shape(agents_root, agents_boundary, "角色目錄")
    _reject_overlapping_roots(skills_root, agents_root, attic)

    skills_targets = [skills_root, attic]
    skills_targets += [skills_root / name
                       for name in SKILLS + [ORCHESTRATOR]]
    for target in skills_targets:
        _validate_directory_destination(target, skills_boundary, "skill 安裝目錄")
    _validate_directory_destination(
        agents_root, agents_boundary, "角色安裝目錄")

    for name in SKILLS + [ORCHESTRATOR]:
        _reject_tree_symlinks(skills_root / name, "既有 skill 目錄")
    _reject_tree_symlinks(attic, "既有備份目錄")

    for name in AGENTS:
        _validate_file_destination(
            agents_root / name, agents_boundary, "agent 目的檔")

    if entry_file is not None:
        if scope == "personal" and entry_file == entry_files[1]:
            entry_boundary = entry_files[1].parent
        else:
            entry_boundary = Path.home() if scope == "personal" else project_root
        if entry_boundary is None:
            raise UnsafeDestinationError("找不到流程入口的允許範圍。")
        _validate_file_destination(entry_file, entry_boundary, "流程入口目的檔")


def confirm(question, default=True):
    hint = "Y/n" if default else "y/N"
    raw = input("\n" + bold(question) + " [{}]: ".format(hint)).strip().lower()
    return default if not raw else raw in ("y", "yes")


# --------------------------------------------------------------------------
# pack integrity
# --------------------------------------------------------------------------

def missing_pack_files():
    """Every file this installer intends to copy, checked before writing.

    A partial unzip or a sync that never finished otherwise installs
    silently and only surfaces weeks later as a half-working phase gate.
    """
    required = [PACK / "skills" / s / "SKILL.md" for s in SKILLS]
    required += [PACK / "agents" / a for a in AGENTS]
    orchestrator = PACK / "skills" / ORCHESTRATOR
    required += [
        orchestrator / "DESIGN.md",
        orchestrator / "SDLC_主流程版_IAO.md",
        orchestrator / "references" / "agent-teams.md",
        orchestrator / "references" / "severity-format.md",
    ]
    phase_skills = [skill for skill in SKILLS if skill != "change-request"]
    required += [
        PACK / "skills" / skill / "references" / "phase-exit-criteria.md"
        for skill in phase_skills
    ]
    missing = [p for p in required if not p.is_file()]
    if not orchestrator.is_dir():
        missing.append(orchestrator)
    return missing


# --------------------------------------------------------------------------
# entry protocol
# --------------------------------------------------------------------------

def extract_entry_protocol():
    """Pull the fenced Entry Protocol block out of the design doc.

    Located by heading text rather than line number so the doc can be
    edited without breaking the installer.
    """
    design = PACK / "skills" / ORCHESTRATOR / "DESIGN.md"
    if not design.is_file():
        return None
    lines = design.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.lstrip().startswith("#") and "Entry Protocol" in ln), None)
    if start is None:
        return None
    fence = next((i for i in range(start, len(lines))
                  if lines[i].startswith("```")), None)
    if fence is None:
        return None
    closing_fence = next((i for i in range(fence + 1, len(lines))
                          if lines[i].startswith("```")), None)
    if closing_fence is None:
        return None
    body = lines[fence + 1:closing_fence]
    return "\n".join(body).strip() or None


def render_entry_protocol(
        protocol: str, skills_root: Path, agents_root: Path) -> str:
    """Bind the portable protocol template to both selected payload roots."""
    replacements = {
        "{{SKILLS_ROOT}}": _absolute_path(skills_root),
        "{{AGENTS_ROOT}}": _absolute_path(agents_root),
    }
    rendered = protocol
    for placeholder, path in replacements.items():
        if placeholder not in rendered:
            raise ValueError(
                "Entry Protocol 缺少 {} 路徑標記".format(placeholder))
        rendered = rendered.replace(placeholder, str(path))
    return rendered


def protocol_already_present(text, protocol):
    """Detect an unmarked copy of the protocol already in the file.

    Matches on distinctive lines rather than the whole block, so a
    hand-pasted copy still counts even if it was reflowed or trimmed.
    """
    lines = [ln.strip() for ln in protocol.splitlines() if len(ln.strip()) > 20]
    if not lines:
        return False
    hits = sum(1 for ln in lines if ln in text)
    return hits >= max(2, len(lines) // 3)


def inject_entry_protocol(target_file, protocol):
    """Insert or refresh the protocol block. Returns a status string."""
    global WROTE_ANYTHING
    if target_file.is_symlink():
        raise UnsafeDestinationError(
            "流程入口目的檔是 symbolic link：{}".format(target_file))
    block = "{}\n\n## SDLC 開發流程入口\n\n{}\n\n{}\n".format(BEGIN, protocol, END)

    if not target_file.exists():
        target_file.parent.mkdir(parents=True, exist_ok=True)
        WROTE_ANYTHING = True
        target_file.write_text(block, encoding="utf-8")
        return "created"

    if not os.access(str(target_file), os.W_OK):
        # Probe before backing up, so a locked file leaves no orphan copy.
        print(red("  {} 沒有權限修改 {}".format(WARN, target_file)))
        print("    " + dim("檔案可能被設為唯讀，或被公司的裝置管理軟體鎖住。"))
        print("    " + dim("解除唯讀後再跑一次，skill 本身已經裝好了。"))
        return "skipped"

    text = target_file.read_text(encoding="utf-8")
    has_begin, has_end = BEGIN in text, END in text

    if has_begin != has_end:
        print(yellow("  {} {} 裡的 SDLC 標記不完整（只有 BEGIN 或只有 END）。".format(
            WARN, target_file.name)))
        print("    " + dim("為避免貼出重複內容，這次不會修改這個檔案。"))
        print("    " + dim("請把那兩行標記補齊或整段刪掉，再跑一次。"))
        return "skipped"

    if not has_begin and protocol_already_present(text, protocol):
        print(yellow("  {} {} 裡已經有流程入口的內容，但沒有 install.py 的標記".format(
            WARN, target_file.name)))
        print("    " + dim("（看起來是之前手動貼上的）。"))
        if not confirm("  仍要再加一份嗎？（選 n 保持原樣，建議）", default=False):
            return "skipped"

    if has_begin and has_end:
        if text.index(END) < text.index(BEGIN):
            print(yellow("  {} {} 裡的 SDLC 標記順序異常（END 出現在 BEGIN 之前）。".format(
                WARN, target_file.name)))
            print("    " + dim("為避免刪掉你的內容，這次不會修改這個檔案。"))
            return "skipped"
        if not confirm("{} 裡已經有舊版流程入口，要更新成這一版嗎？".format(target_file.name)):
            return "skipped"
        backup(target_file)
        WROTE_ANYTHING = True
        head, _, rest = text.partition(BEGIN)
        _, _, tail = rest.partition(END)
        target_file.write_text(head + block + tail.lstrip("\n"), encoding="utf-8")
        return "updated"

    backup(target_file)
    WROTE_ANYTHING = True
    joiner = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    target_file.write_text(text + joiner + "\n" + block, encoding="utf-8")
    return "appended"


def unique_backup_name(path):
    """A timestamped sibling name that is not already taken."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = path.with_name("{}.backup-{}{}".format(path.stem, stamp, path.suffix))
    n = 2
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(
            "{}.backup-{}-{}{}".format(path.stem, stamp, n, path.suffix))
        n += 1
    return candidate


def backup(path):
    if path.is_symlink():
        raise UnsafeDestinationError("拒絕備份 symbolic link：{}".format(path))
    dest = unique_backup_name(path)
    shutil.copy2(str(path), str(dest))
    print(dim("      已備份原檔 → {}".format(dest.name)))
    return dest


# --------------------------------------------------------------------------
# copying
# --------------------------------------------------------------------------

def dir_differs(src, dst):
    """True if dst holds anything the pack would not put there."""
    for f in src.rglob("*"):
        if f.is_dir() or f.name == ".DS_Store":
            continue
        counterpart = dst / f.relative_to(src)
        if not counterpart.is_file() or counterpart.read_bytes() != f.read_bytes():
            return True
    for f in dst.rglob("*"):
        if f.is_file() and f.name != ".DS_Store" and not (src / f.relative_to(dst)).exists():
            return True  # something the user added
    return False


def copy_tree(src, dst, attic):
    """Install src at dst, preserving anything already living there.

    Whatever is displaced moves *out* of skills/ rather than being renamed
    in place: any directory holding a SKILL.md is loaded as a skill, so a
    backup left alongside would register a second skill under the same name.
    """
    global WROTE_ANYTHING
    replaced = None
    if dst.exists():
        if not dir_differs(src, dst):
            return None
        attic.mkdir(parents=True, exist_ok=True)
        replaced = unique_backup_name(attic / dst.name)
        shutil.move(str(dst), str(replaced))
    WROTE_ANYTHING = True
    shutil.copytree(str(src), str(dst),
                    ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"))
    return replaced


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    global WROTE_ANYTHING
    print(bold("\n  SDLC 開發流程包 — 安裝程式"))
    print(dim("  9 個流程 skill + 3 個角色定義 + 流程入口"))

    missing = missing_pack_files()
    if missing:
        print(red("\n{} 這個包不完整，缺少：".format(CROSS)))
        for path in missing:
            print("    " + str(path.relative_to(PACK)))
        print("  " + dim("可能是解壓縮沒完成，或檔案在傳輸中遺失。"))
        print("  請重新解壓縮，或向提供這個包的人重新索取。")
        return 1
    protocol_template = extract_entry_protocol()
    if protocol_template is None:
        print(red("\n{} 這個包不完整：找不到有效的 Entry Protocol。".format(CROSS)))
        print("  " + dim("尚未寫入任何檔案。請重新取得完整安裝包。"))
        return 1
    missing_placeholders = [
        marker for marker in ("{{SKILLS_ROOT}}", "{{AGENTS_ROOT}}")
        if marker not in protocol_template
    ]
    if missing_placeholders:
        print(red("\n{} 這個包不完整：Entry Protocol 缺少路徑標記：{}。".format(
            CROSS, "、".join(missing_placeholders))))
        print("  " + dim("尚未寫入任何檔案。請重新取得完整安裝包。"))
        return 1

    # ---- 1. personal or project scope ----------------------------------
    heading("步驟 1 / 4 — 選擇安裝範圍")
    print("  " + dim("個人安裝會套用到所有專案；專案安裝只會套用到指定專案。"))
    scope, project_root = choose_install_scope()
    try:
        if scope == "project":
            project_root = normalized_project_root(project_root)
        entry_files = entry_file_locations(scope, project_root)
    except ValueError as exc:
        heading("安裝前安全檢查未通過")
        print(red("  {} {}".format(CROSS, exc)))
        print("  " + dim("尚未寫入任何檔案。請改選真正的專案根目錄。"))
        return 1

    # ---- 2. where the entry protocol goes -------------------------------
    heading("步驟 2 / 4 — 流程入口要寫進哪個檔案")
    print("  " + dim("這段文字告訴 AI「動工前先看 docs/ 判斷現在在哪個階段」。"))
    print("  " + dim("下面只列出與剛才安裝範圍相同的 Claude Code / Codex 規則檔。"))
    if scope == "personal":
        options = [
            ("個人／全域 CLAUDE.md（Claude Code，用於所有專案）",
             str(entry_files[0])),
            ("個人／全域 AGENTS.md（Codex，用於所有專案）",
             "{}　遵循 CODEX_HOME，未設定時使用 ~/.codex".format(entry_files[1])),
        ]
    else:
        options = [
            ("這個專案的 CLAUDE.md（Claude Code 用）", str(entry_files[0])),
            ("這個專案的 AGENTS.md（Codex 用）", str(entry_files[1])),
        ]
    choice = ask_choice("寫進哪裡？", options, default=1)
    entry_file = entry_files[choice - 1]
    entry_platform = "claude" if choice == 1 else "codex"

    # ---- 3. where skills and role definitions go -----------------------
    heading("步驟 3 / 4 — 分別選擇 skill 與角色檔位置")
    print("  " + dim("兩者可以依個人習慣分開選；每一題都會先推薦與規則檔相符的位置。"))
    skills_root, skills_boundary, _ = choose_storage_root(
        "skills", scope, entry_platform, project_root)
    agents_root, agents_boundary, _ = choose_storage_root(
        "agents", scope, entry_platform, project_root)
    attic = skills_root.parent / "sdlc-replaced-backups"
    print("\n  skill 將安裝到：{}".format(bold(str(skills_root))))
    print("  角色檔將安裝到：{}".format(bold(str(agents_root))))

    try:
        protocol = render_entry_protocol(
            protocol_template, skills_root, agents_root)
    except ValueError as exc:
        print(red("\n{} 流程入口樣板不完整：{}".format(CROSS, exc)))
        print("  " + dim("尚未寫入任何檔案。請重新取得完整安裝包。"))
        return 1

    try:
        preflight_installation(
            scope, project_root, skills_root, agents_root, attic,
            skills_boundary, agents_boundary, entry_file, entry_files)
    except UnsafeDestinationError as exc:
        heading("安裝前安全檢查未通過")
        print(red("  {} {}".format(CROSS, exc)))
        print("  " + dim("尚未寫入任何檔案。請修正路徑後重新執行安裝程式。"))
        return 1

    # ---- 4. install -----------------------------------------------------
    heading("步驟 4 / 4 — 開始安裝")
    skills_root.mkdir(parents=True, exist_ok=True)
    agents_root.mkdir(parents=True, exist_ok=True)

    preserved = []

    for name in SKILLS + [ORCHESTRATOR]:
        kept = copy_tree(PACK / "skills" / name, skills_root / name, attic)
        if kept:
            preserved.append(kept)
            print("  {} skills/{}  {}".format(
                green(TICK), name, yellow("（原有的同名 skill 已移到 {}/）".format(attic.name))))
        else:
            print("  {} skills/{}".format(green(TICK), name))

    for name in AGENTS:
        src, dst = PACK / "agents" / name, agents_root / name
        if dst.is_symlink():
            raise UnsafeDestinationError("agent 目的檔是 symbolic link：{}".format(dst))
        if dst.is_file() and dst.read_bytes() != src.read_bytes():
            preserved.append(backup(dst))
        WROTE_ANYTHING = True
        shutil.copy2(str(src), str(dst))
        print("  {} agents/{}".format(green(TICK), name))

    entry_status = None
    if entry_file is not None:
        entry_status = inject_entry_protocol(entry_file, protocol)
        label = {"created": "已建立", "appended": "已附加到",
                 "updated": "已更新", "skipped": "略過（保留原樣）"}[entry_status]
        mark = green(TICK) if entry_status != "skipped" else yellow("-")
        print("  {} 流程入口 {} {}".format(mark, label, entry_file.name))

    # ---- report ---------------------------------------------------------
    heading("完成")
    print("  skill：{}".format(bold(str(skills_root))))
    print("    {} 個流程 skill + {}/（共用參照）".format(
        len(SKILLS), ORCHESTRATOR))
    print("  角色檔：{}".format(bold(str(agents_root))))
    print("    {} 個角色定義".format(len(AGENTS)))
    if entry_file is not None and entry_status != "skipped":
        print("  流程入口：{}".format(bold(str(entry_file))))

    if preserved:
        print("\n  " + yellow("{} 你原本就有同名的檔案／skill，沒有被刪除，已移到：".format(WARN)))
        for p in preserved:
            print("    " + str(p))
        print("  " + dim("那可能是你自己的同名 skill（名稱通用時容易撞名），"))
        print("  " + dim("也可能只是你改過的舊版。請打開確認後再決定要不要刪。"))

    heading("確認裝好了")
    print("  1. 完全關閉並重新開啟 Claude Code / Codex")
    print("  2. 輸入 " + bold("/") + " 應該能看到這 9 個 skill：")
    print(dim("     " + "、".join(SKILLS)))
    print("  3. 或直接說「我想開發一個新功能」，它應該先去看 docs/ 資料夾，")
    print(dim("     而不是直接開始寫程式。"))
    print("\n  " + dim("看不到？先確認 skill 位於 {}，並已完全重啟工具。".format(
        skills_root)))
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        if WROTE_ANYTHING:
            print("\n\n已中斷。" + yellow("注意：部分檔案已經寫入（見上方勾選的項目），安裝並不完整。"))
            print("再跑一次就會補齊。\n")
        else:
            print("\n\n已取消，沒有變更任何檔案。\n")
        sys.exit(130)
    except PermissionError as exc:
        print(red("\n\n沒有權限寫入：{}".format(exc.filename or exc)))
        print("  " + dim("可能是資料夾唯讀，或被公司的裝置管理軟體鎖住。"))
        print("  " + dim("換一個你有權限的位置，或請 IT 解除限制後再跑一次。\n"))
        sys.exit(1)
    except OSError as exc:
        print(red("\n\n檔案操作失敗：{}".format(exc)))
        print("  " + dim("請把上面這行連同你執行的指令一起回報給提供這個包的人。\n"))
        sys.exit(1)
