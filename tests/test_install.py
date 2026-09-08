import io
import re
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import install


def _phase_skill():
    """第一個真的有 phase-exit-criteria.md 的 skill。

    直接寫 SKILLS[0] 會被清單順序綁死——converge 排進第一個之後，
    刪它的 phase-exit-criteria.md 不會觸發任何錯誤（它本來就沒有那份檔），
    那個 case 就變成永遠不會失敗的假測試。
    """
    for skill in install.SKILLS:
        if skill not in install.NO_EXIT_CRITERIA:
            return skill
    raise AssertionError("SKILLS 裡沒有任何帶 phase-exit-criteria 的 skill")


class InstallLocationTests(unittest.TestCase):
    def setUp(self):
        self.original_wrote_anything = install.WROTE_ANYTHING
        install.WROTE_ANYTHING = False

    def tearDown(self):
        install.WROTE_ANYTHING = self.original_wrote_anything

    def make_symlink(self, target, link, target_is_directory=False):
        try:
            link.symlink_to(target, target_is_directory=target_is_directory)
        except (NotImplementedError, OSError) as exc:
            self.skipTest("symbolic links are unavailable: {}".format(exc))

    def run_main(self, answers, fake_home, environ=None, pack=None):
        output = io.StringIO()
        patches = [
            mock.patch.object(install.Path, "home", return_value=fake_home),
            mock.patch.dict(os.environ, environ or {}, clear=True),
            mock.patch("builtins.input", side_effect=answers),
        ]
        if pack is not None:
            patches.append(mock.patch.object(install, "PACK", pack))
        with patches[0], patches[1], patches[2], \
                (patches[3] if len(patches) == 4 else mock.patch.object(
                    install, "PACK", install.PACK)), redirect_stdout(output):
            result = install.main()
        return result, output.getvalue()

    def make_complete_fixed_pack(self, root, name):
        pack = root / name
        for skill in install.SKILLS:
            skill_dir = pack / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
            if skill not in install.NO_EXIT_CRITERIA:
                reference_dir = skill_dir / "references"
                reference_dir.mkdir()
                (reference_dir / "phase-exit-criteria.md").write_text(
                    "# Exit criteria\n", encoding="utf-8")
        orchestrator = pack / "skills" / install.ORCHESTRATOR
        orchestrator.mkdir(parents=True)
        (orchestrator / "DESIGN.md").write_text(
            "### Entry Protocol\n\n```\nSkill root: {{SKILLS_ROOT}}\n"
            "Agent root: {{AGENTS_ROOT}}\n```\n",
            encoding="utf-8")
        (orchestrator / "SDLC_主流程版_IAO.md").write_text(
            "# IAO\n", encoding="utf-8")
        shared_references = orchestrator / "references"
        shared_references.mkdir()
        (shared_references / "agent-teams.md").write_text(
            "# Agent teams\n", encoding="utf-8")
        (shared_references / "severity-format.md").write_text(
            "# Severity\n", encoding="utf-8")
        (shared_references / "questioning-sufficiency.md").write_text(
            "# Questioning sufficiency\n", encoding="utf-8")
        (shared_references / "ticket-spec.md").write_text(
            "# Ticket spec\n", encoding="utf-8")
        (shared_references / "framework-defects.md").write_text(
            "# Framework defects\n", encoding="utf-8")
        (shared_references / "tailoring.md").write_text(
            "# Tailoring\n", encoding="utf-8")
        (shared_references / "traceability.md").write_text(
            "# Traceability\n", encoding="utf-8")
        (shared_references / "test-case-coverage.md").write_text(
            "# Test case coverage\n", encoding="utf-8")
        (shared_references / "phase-transition-reminders.md").write_text(
            "# Phase transition reminders\n", encoding="utf-8")
        (shared_references / "tooling-reuse.md").write_text(
            "# Tooling reuse\n", encoding="utf-8")
        (orchestrator / "CHANGELOG.md").write_text(
            "# Changelog\n", encoding="utf-8")
        (orchestrator / "sdlc-entry.md").write_text(
            "# Step 0\n", encoding="utf-8")
        (orchestrator / "claude_sdlc.md").write_text(
            "# Paste-in entry table\n", encoding="utf-8")
        agents = pack / "agents"
        agents.mkdir()
        for agent in install.AGENTS:
            (agents / agent).write_text("# Agent\n", encoding="utf-8")
        return pack

    def test_personal_scope_does_not_ask_for_project_root(self):
        with mock.patch.object(install, "ask_choice", return_value=1), \
                mock.patch.object(install, "ask_project_root") as ask_project_root:
            scope, project_root = install.choose_install_scope()

        self.assertEqual("personal", scope)
        self.assertIsNone(project_root)
        ask_project_root.assert_not_called()

    def test_personal_entry_files_use_global_claude_and_default_codex_homes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            entry_files = install.entry_file_locations(
                "personal", home=home, environ={})

        self.assertEqual(
            [home / ".claude" / "CLAUDE.md", home / ".codex" / "AGENTS.md"],
            entry_files,
        )
        self.assertEqual(2, len(set(entry_files)))

    def test_personal_entry_files_honor_codex_home(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            custom_codex_home = home / "custom-codex"
            entry_files = install.entry_file_locations(
                "personal", home=home,
                environ={"CODEX_HOME": str(custom_codex_home)})

        self.assertEqual(
            Path(os.path.abspath(str(custom_codex_home))) / "AGENTS.md",
            entry_files[1],
        )

    def test_standard_storage_roots_cover_both_tools_kinds_and_scopes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            project = root / "project"
            cases = (
                ("personal", "claude", None, home / ".claude"),
                ("personal", "codex", None, home / ".agents"),
                ("project", "claude", project, project.resolve() / ".claude"),
                ("project", "codex", project, project.resolve() / ".agents"),
            )
            for scope, platform, project_root, base in cases:
                with self.subTest(scope=scope, platform=platform):
                    for kind in ("skills", "agents"):
                        storage, boundary = install.standard_storage_root(
                            scope, platform, kind,
                            project_root=project_root, home=home)
                        self.assertEqual(base / kind, storage)
                        self.assertEqual(
                            home if scope == "personal" else project.resolve(),
                            boundary)

    def test_project_entry_files_stay_at_project_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            entry_files = install.entry_file_locations(
                "project", project_root=project)

        self.assertEqual(
            [project.resolve() / "CLAUDE.md", project.resolve() / "AGENTS.md"],
            entry_files)

    def test_storage_recommendation_is_first_for_selected_rule_platform(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            for platform, expected in (
                    ("claude", project.resolve() / ".claude" / "skills"),
                    ("codex", project.resolve() / ".agents" / "skills")):
                with self.subTest(platform=platform), \
                        mock.patch.object(
                            install, "ask_choice", return_value=1) as ask_choice:
                    locations = install.choose_storage_root(
                        "skills", "project", platform, project)
                options = ask_choice.call_args.args[1]
                self.assertIn("建議", options[0][0])
                self.assertIn(str(expected), options[0][1])
                self.assertEqual(expected, locations[0])

    def test_storage_custom_path_is_asked_only_for_the_custom_choice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            custom = project / "my-skills"
            # 選項 1 = 與步驟 2 相符的標準位置 → 不該問路徑
            with mock.patch.object(install, "ask_choice", return_value=1), \
                    mock.patch.object(install, "ask_path") as ask_path:
                install.choose_storage_root(
                    "skills", "project", "claude", project)
                ask_path.assert_not_called()
            # 選項 2 = 自訂絕對路徑 → 才問（跨平台那個選項已移除）
            with mock.patch.object(install, "ask_choice", return_value=2), \
                    mock.patch.object(install, "ask_path", return_value=custom) as ask_path:
                selected, boundary, source = install.choose_storage_root(
                    "skills", "project", "claude", project)
            ask_path.assert_called_once()
            question, hint = ask_path.call_args.args
            self.assertIn("完整絕對", question)
            self.assertIn("不要輸入 .agents/skills", hint)
            self.assertEqual(custom.resolve(), selected)
            self.assertEqual(project.resolve(), boundary)
            self.assertEqual("custom", source)

    def test_project_prompt_rejects_all_tool_config_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "project"
            invalid = [
                project / ".claude",
                project / ".CoDeX" / "nested",
                project / ".agents" / "nested" / "deeper",
            ]
            for path in invalid:
                path.mkdir(parents=True)
            output = io.StringIO()
            answers = tuple(str(path) for path in invalid) + (str(project),)
            with mock.patch("builtins.input", side_effect=answers), \
                    redirect_stdout(output):
                selected = install.ask_project_root()

        self.assertEqual(project.resolve(), selected)
        self.assertEqual(3, output.getvalue().count("工具設定資料夾"))

    def test_config_directories_cannot_be_used_as_project_roots(self):
        config_paths = (
            Path("project") / ".claude",
            Path("project") / ".codex" / "nested",
            Path("project") / ".AGENTS" / "nested" / "deeper",
        )
        for config_path in config_paths:
            with self.subTest(config_path=config_path):
                with self.assertRaises(ValueError):
                    install.entry_file_locations(
                        "project", project_root=config_path)
                with self.assertRaises(ValueError):
                    install.standard_storage_root(
                        "project", "codex", "skills", project_root=config_path)

    def test_project_symlink_aliases_to_tool_config_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            targets = (
                root / "workspace" / ".claude",
                root / "workspace" / ".CoDeX" / "nested",
                root / "workspace" / ".AgEnTs" / "nested" / "deeper",
            )
            aliases = []
            for index, target in enumerate(targets):
                target.mkdir(parents=True)
                alias = root / "alias-{}".format(index)
                self.make_symlink(target, alias, target_is_directory=True)
                aliases.append(alias)

            for alias in aliases:
                with self.subTest(alias=alias):
                    with self.assertRaises(ValueError):
                        install.entry_file_locations(
                            "project", project_root=alias)
                    with self.assertRaises(ValueError):
                        install.standard_storage_root(
                            "project", "codex", "skills", project_root=alias)

            safe_project = root / "safe-project"
            safe_project.mkdir()
            output = io.StringIO()
            answers = tuple(str(alias) for alias in aliases) + (str(safe_project),)
            with mock.patch("builtins.input", side_effect=answers), \
                    redirect_stdout(output):
                selected = install.ask_project_root()

        self.assertEqual(safe_project.resolve(), selected)
        self.assertEqual(3, output.getvalue().count("工具設定資料夾"))

    def test_main_rejects_project_alias_to_tool_config_before_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_home = root / "home"
            config_dir = root / "workspace" / ".agents" / "nested"
            alias = root / "innocent-project-name"
            fake_home.mkdir()
            config_dir.mkdir(parents=True)
            self.make_symlink(config_dir, alias, target_is_directory=True)
            output = io.StringIO()
            with mock.patch.object(install.Path, "home", return_value=fake_home), \
                    mock.patch.object(install, "ask_project_root", return_value=alias), \
                    mock.patch("builtins.input", side_effect=("2",)), \
                    redirect_stdout(output):
                result = install.main()

            self.assertEqual(1, result)
            self.assertFalse((config_dir / ".agents").exists())
            self.assertFalse((config_dir / "AGENTS.md").exists())
            self.assertFalse(install.WROTE_ANYTHING)
            self.assertIn("尚未寫入任何檔案", output.getvalue())

    def test_main_normal_project_symlink_uses_resolved_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_home = root / "home"
            project = root / "real-project"
            alias = root / "project-alias"
            fake_home.mkdir()
            project.mkdir()
            self.make_symlink(project, alias, target_is_directory=True)
            result, output = self.run_main(
                ("2", str(alias), "2", "", ""), fake_home)

            self.assertEqual(0, result)
            self.assertTrue((project / ".agents" / "skills" /
                             "product-discovery" / "SKILL.md").is_file())
            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertIn(str(project.resolve()), output)

    def test_main_personal_claude_default_writes_only_under_fake_home(self):
        real_home = Path.home()
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_home = Path(temp_dir) / "home"
            fake_home.mkdir()
            result, output = self.run_main(("", "", "", ""), fake_home)

            self.assertEqual(0, result)
            skills_root = fake_home / ".claude" / "skills"
            self.assertTrue((skills_root / "product-discovery" / "SKILL.md").is_file())
            self.assertTrue((fake_home / ".claude" / "agents" /
                             "sdlc-implementer.md").is_file())
            entry = fake_home / ".claude" / "CLAUDE.md"
            self.assertTrue(entry.is_file())
            self.assertIn(str(skills_root), entry.read_text(encoding="utf-8"))
            self.assertNotIn("{{SKILLS_ROOT}}", entry.read_text(encoding="utf-8"))
            self.assertFalse((fake_home / ".agents").exists())
            self.assertNotEqual(real_home, fake_home)
            self.assertIn("步驟 3 / 4", output)

    def test_main_project_claude_default_reprompts_for_config_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            fake_home.mkdir()
            project = sandbox / "project"
            config_dir = project / ".claude"
            config_dir.mkdir(parents=True)
            answers = ("2", str(config_dir), str(project), "1", "", "")
            result, output = self.run_main(answers, fake_home)

            self.assertEqual(0, result)
            self.assertTrue((project / ".claude" / "skills" /
                             "product-discovery" / "SKILL.md").is_file())
            self.assertTrue((project / "CLAUDE.md").is_file())
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertFalse((project / ".agents").exists())
            self.assertIn("工具設定資料夾", output)
            self.assertIn("這個專案的 AGENTS.md", output)

    def test_main_empty_project_agents_default_creates_full_codex_chain(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "empty-project"
            fake_home.mkdir()
            project.mkdir()
            self.assertFalse((project / ".agents").exists())
            result, output = self.run_main(
                ("2", str(project), "2", "", ""), fake_home)

            self.assertEqual(0, result)
            skills_root = project / ".agents" / "skills"
            agents_root = project / ".agents" / "agents"
            self.assertTrue((skills_root / "product-discovery" / "SKILL.md").is_file())
            self.assertTrue((agents_root / "sdlc-reviewer.md").is_file())
            entry = project / "AGENTS.md"
            self.assertTrue(entry.is_file())
            entry_text = entry.read_text(encoding="utf-8")
            self.assertIn(str(skills_root), entry_text)
            self.assertNotIn("{{SKILLS_ROOT}}", entry_text)
            self.assertNotIn("{{AGENTS_ROOT}}", entry_text)
            self.assertIn(str(agents_root), entry_text)
            self.assertFalse((project / ".claude").exists())
            self.assertIn("Codex 標準位置（建議", output)

    def test_storage_choices_never_offer_the_other_platform(self):
        """步驟 2 選了哪個平台，步驟 3 就只給那個平台的標準位置。

        舊行為讓人可以把規則檔寫進 AGENTS.md（Codex）、卻把 skill 裝到
        .claude/skills（Claude Code 的位置）。該平台不會自動載入另一個平台的
        目錄，等於裝了卻不會被叫到；而規則裡若有任何路徑引用，也會指向
        不存在的地方。這個組合已移除，本測試確保它不會被加回來。
        """
        project = Path("/tmp/does-not-need-to-exist")
        for entry_platform, forbidden in (("claude", ".agents"),
                                          ("codex", ".claude")):
            for kind in ("skills", "agents"):
                with self.subTest(platform=entry_platform, kind=kind):
                    captured = []
                    with mock.patch.object(
                            install, "ask_choice",
                            side_effect=lambda q, opts, default=1: (
                                captured.append(opts) or 1)):
                        install.choose_storage_root(
                            kind, "project", entry_platform, project)
                    rendered = " ".join(
                        "{} {}".format(label, detail)
                        for label, detail in captured[0])
                    self.assertNotIn(
                        forbidden + "/" + kind, rendered,
                        "步驟 2 選 {} 之後，步驟 3 不該再出現 {} 的標準位置："
                        "{}".format(entry_platform, forbidden, rendered))
                    self.assertEqual(
                        2, len(captured[0]),
                        "只該有『相符的標準位置』與『自訂路徑』兩個選項，"
                        "實際 {} 個".format(len(captured[0])))

    def test_main_same_platform_roots_are_both_used(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            fake_home.mkdir()
            project.mkdir()
            result, _ = self.run_main(
                ("2", str(project), "2", "1", "1"), fake_home)

            skills_root = project / ".agents" / "skills"
            agents_root = project / ".agents" / "agents"
            entry_text = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(0, result)
            self.assertTrue((skills_root / "qa-handoff" / "SKILL.md").is_file())
            self.assertTrue((agents_root / "sdlc-reviewer.md").is_file())
            self.assertIn(str(skills_root), entry_text)
            self.assertIn(str(agents_root), entry_text)
            self.assertNotIn("{{SKILLS_ROOT}}", entry_text)
            self.assertNotIn("{{AGENTS_ROOT}}", entry_text)

    def test_main_custom_skill_root_is_created_after_preflight(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            custom_skills = project / "team-layout" / "skills"
            fake_home.mkdir()
            project.mkdir()
            result, _ = self.run_main(
                ("2", str(project), "2", "2", str(custom_skills), "yes", ""),
                fake_home)

            self.assertEqual(0, result)
            self.assertTrue((custom_skills / "system-design" / "SKILL.md").is_file())
            self.assertIn(
                str(custom_skills),
                (project / "AGENTS.md").read_text(encoding="utf-8"))

    def test_main_custom_skill_and_agent_roots_are_independent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            custom_skills = project / "my-layout" / "skill-library"
            custom_agents = project / "my-layout" / "role-library"
            fake_home.mkdir()
            project.mkdir()
            result, _ = self.run_main(
                ("2", str(project), "2",
                 "2", str(custom_skills), "yes",
                 "2", str(custom_agents), "yes"),
                fake_home)

            self.assertEqual(0, result)
            self.assertTrue(
                (custom_skills / "qa-handoff" / "SKILL.md").is_file())
            self.assertTrue(
                (custom_agents / "sdlc-verifier.md").is_file())
            entry_text = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(str(custom_skills.resolve()), entry_text)
            self.assertIn(str(custom_agents.resolve()), entry_text)
            self.assertNotIn("{{SKILLS_ROOT}}", entry_text)
            self.assertNotIn("{{AGENTS_ROOT}}", entry_text)

    def test_main_personal_custom_skill_root_stays_inside_home(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_home = Path(temp_dir) / "home"
            custom_skills = fake_home / "my-sdlc" / "skills"
            fake_home.mkdir()
            result, _ = self.run_main(
                ("", "", "2", str(custom_skills), "yes", ""),
                fake_home)

            self.assertEqual(0, result)
            self.assertTrue(
                (custom_skills.resolve() / "dev-setup" / "SKILL.md").is_file())
            entry_text = (fake_home / ".claude" / "CLAUDE.md").read_text(
                encoding="utf-8")
            self.assertIn(str(custom_skills.resolve()), entry_text)
            self.assertIn(
                str(fake_home / ".claude" / "agents"), entry_text)

    def test_preflight_rejects_unsafe_custom_root_shapes_without_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "project"
            project.mkdir()
            cases = (
                (project, project / "roles"),
                (project / ".agents", project / "roles"),
                (project / "shared", project / "shared"),
                (project / "shared", project / "shared" / "roles"),
                (project.parent / "outside", project / "roles"),
            )
            for skills_root, agents_root in cases:
                with self.subTest(skills_root=skills_root, agents_root=agents_root):
                    attic = skills_root.parent / "sdlc-replaced-backups"
                    with self.assertRaises(install.UnsafeDestinationError):
                        install.preflight_installation(
                            "project", project, skills_root, agents_root, attic,
                            project, project, None,
                            [project / "CLAUDE.md", project / "AGENTS.md"])
                    self.assertFalse(install.WROTE_ANYTHING)
                    self.assertFalse((project / "CLAUDE.md").exists())
                    self.assertFalse((project / "AGENTS.md").exists())

    def test_main_personal_codex_default_uses_agents_and_codex_home(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            codex_home = sandbox / "codex-home"
            fake_home.mkdir()
            result, _ = self.run_main(
                ("", "2", "", ""), fake_home,
                environ={"CODEX_HOME": str(codex_home)})

            self.assertEqual(0, result)
            skills_root = fake_home / ".agents" / "skills"
            self.assertTrue((skills_root / "system-design" / "SKILL.md").is_file())
            self.assertTrue((fake_home / ".agents" / "agents" /
                             "sdlc-verifier.md").is_file())
            self.assertIn(
                str(skills_root),
                (codex_home / "AGENTS.md").read_text(encoding="utf-8"),
            )
            self.assertFalse((fake_home / ".claude").exists())

    def test_main_rejects_codex_home_regular_file_before_payload_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_home = root / "home"
            codex_home_file = root / "codex-home"
            fake_home.mkdir()
            codex_home_file.write_bytes(b"keep codex home bytes")
            result, output = self.run_main(
                ("", "2", "", ""), fake_home,
                environ={"CODEX_HOME": str(codex_home_file)})

            self.assertEqual(1, result)
            self.assertEqual(b"keep codex home bytes", codex_home_file.read_bytes())
            self.assertFalse((fake_home / ".agents").exists())
            self.assertFalse(install.WROTE_ANYTHING)
            self.assertIn("允許範圍不是資料夾", output)
            self.assertIn("尚未寫入任何檔案", output)

    def test_main_rejects_codex_home_below_regular_file_before_payload_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_home = root / "home"
            blocker = root / "codex-home-blocker"
            fake_home.mkdir()
            blocker.write_bytes(b"keep blocker bytes")
            codex_home = blocker / "child"
            result, output = self.run_main(
                ("", "2", "", ""), fake_home,
                environ={"CODEX_HOME": str(codex_home)})

            self.assertEqual(1, result)
            self.assertEqual(b"keep blocker bytes", blocker.read_bytes())
            self.assertFalse((fake_home / ".agents").exists())
            self.assertFalse(install.WROTE_ANYTHING)
            self.assertIn("既有上層不是資料夾", output)
            self.assertIn("尚未寫入任何檔案", output)

    def test_main_rejects_project_claude_directory_symlink_before_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            outside = sandbox / "outside"
            fake_home.mkdir()
            project.mkdir()
            outside.mkdir()
            self.make_symlink(outside, project / ".claude", target_is_directory=True)
            result, output = self.run_main(
                ("2", str(project), "1", "", ""), fake_home)

            self.assertEqual(1, result)
            self.assertEqual([], list(outside.iterdir()))
            self.assertFalse((project / "CLAUDE.md").exists())
            self.assertFalse(install.WROTE_ANYTHING)
            self.assertIn("symbolic link", output)
            self.assertIn("尚未寫入任何檔案", output)

    def test_main_rejects_entry_file_symlink_without_touching_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            outside_file = sandbox / "outside-CLAUDE.md"
            fake_home.mkdir()
            project.mkdir()
            outside_file.write_bytes(b"keep these bytes")
            self.make_symlink(outside_file, project / "CLAUDE.md")
            result, _ = self.run_main(
                ("2", str(project), "1", "", ""), fake_home)

            self.assertEqual(1, result)
            self.assertEqual(b"keep these bytes", outside_file.read_bytes())
            self.assertFalse((project / ".claude").exists())
            self.assertFalse(install.WROTE_ANYTHING)

    def test_main_rejects_broken_agent_symlink_before_creating_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            agents_dir = project / ".claude" / "agents"
            missing_target = sandbox / "outside" / "missing-agent.md"
            fake_home.mkdir()
            agents_dir.mkdir(parents=True)
            missing_target.parent.mkdir()
            self.make_symlink(
                missing_target, agents_dir / "sdlc-implementer.md")
            result, _ = self.run_main(
                ("2", str(project), "1", "", ""), fake_home)

            self.assertEqual(1, result)
            self.assertFalse(missing_target.exists())
            self.assertFalse((project / ".claude" / "skills").exists())
            self.assertFalse((project / "CLAUDE.md").exists())
            self.assertFalse(install.WROTE_ANYTHING)

    def test_main_rejects_config_file_collision_before_partial_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            fake_home.mkdir()
            project.mkdir()
            collision = project / ".agents"
            collision.write_text("not a directory", encoding="utf-8")
            result, output = self.run_main(
                ("2", str(project), "2", "", ""), fake_home)

            self.assertEqual(1, result)
            self.assertEqual("not a directory", collision.read_text(encoding="utf-8"))
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertFalse(install.WROTE_ANYTHING)
            self.assertIn("上層路徑不是資料夾", output)

    def test_missing_fixed_pack_files_fail_before_prompts_or_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            cases = {
                "skill": Path("skills") / install.SKILLS[1] / "SKILL.md",
                "agent": Path("agents") / install.AGENTS[1],
                "design": Path("skills") / install.ORCHESTRATOR / "DESIGN.md",
                "iao": (Path("skills") / install.ORCHESTRATOR /
                        "SDLC_主流程版_IAO.md"),
                "agent-teams": (Path("skills") / install.ORCHESTRATOR /
                                "references" / "agent-teams.md"),
                "severity": (Path("skills") / install.ORCHESTRATOR /
                             "references" / "severity-format.md"),
                "phase-exit": (Path("skills") / _phase_skill() /
                               "references" / "phase-exit-criteria.md"),
                "questioning": (Path("skills") / install.ORCHESTRATOR /
                                "references" / "questioning-sufficiency.md"),
                "ticket-spec": (Path("skills") / install.ORCHESTRATOR /
                                "references" / "ticket-spec.md"),
                "framework-defects": (Path("skills") / install.ORCHESTRATOR /
                                      "references" / "framework-defects.md"),
                # 入口文字第一句就指向 tailoring；缺它，「沒有宣告檔＝全跑」
                # 這條預設沒有出處。traceability 被四個地方引用。
                "tailoring": (Path("skills") / install.ORCHESTRATOR /
                              "references" / "tailoring.md"),
                "traceability": (Path("skills") / install.ORCHESTRATOR /
                                 "references" / "traceability.md"),
                "sdlc-entry": (Path("skills") / install.ORCHESTRATOR /
                               "sdlc-entry.md"),
                "claude-sdlc": (Path("skills") / install.ORCHESTRATOR /
                                "claude_sdlc.md"),
            }
            for case, relative in cases.items():
                with self.subTest(case=case):
                    pack = self.make_complete_fixed_pack(sandbox, case)
                    (pack / relative).unlink()
                    output = io.StringIO()
                    with mock.patch.object(install, "PACK", pack), \
                            mock.patch("builtins.input") as input_mock, \
                            redirect_stdout(output):
                        result = install.main()
                    self.assertEqual(1, result)
                    input_mock.assert_not_called()
                    self.assertFalse(install.WROTE_ANYTHING)
                    self.assertIn("這個包不完整", output.getvalue())

    def test_malformed_entry_protocol_fails_before_prompts_or_writes(self):
        malformed = {
            "missing-heading": "# Design without protocol\n",
            "missing-opening": "### Entry Protocol\nno fence\n",
            "missing-closing": (
                "### Entry Protocol\n\n```\nSkill root: {{SKILLS_ROOT}}\n"),
            "missing-placeholder": (
                "### Entry Protocol\n\n```\nSkill root is missing\n```\n"),
            "missing-agent-placeholder": (
                "### Entry Protocol\n\n```\n"
                "Skill root: {{SKILLS_ROOT}}\n```\n"),
            "missing-skill-placeholder": (
                "### Entry Protocol\n\n```\n"
                "Agent root: {{AGENTS_ROOT}}\n```\n"),
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            for case, design_text in malformed.items():
                with self.subTest(case=case):
                    pack = self.make_complete_fixed_pack(sandbox, case)
                    design = (pack / "skills" / install.ORCHESTRATOR /
                              "DESIGN.md")
                    design.write_text(design_text, encoding="utf-8")
                    output = io.StringIO()
                    with mock.patch.object(install, "PACK", pack), \
                            mock.patch("builtins.input") as input_mock, \
                            redirect_stdout(output):
                        result = install.main()
                    self.assertEqual(1, result)
                    input_mock.assert_not_called()
                    self.assertFalse(install.WROTE_ANYTHING)
                    self.assertIn("Entry Protocol", output.getvalue())

    def test_main_rejects_codex_home_broken_symlink_before_payload_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fake_home = root / "home"
            missing_target = root / "missing-codex-home"
            broken_link = root / "codex-home-link"
            fake_home.mkdir()
            self.make_symlink(missing_target, broken_link, target_is_directory=True)
            for configured in (broken_link, broken_link / "child"):
                with self.subTest(configured=configured):
                    install.WROTE_ANYTHING = False
                    result, output = self.run_main(
                        ("", "2", "", ""), fake_home,
                        environ={"CODEX_HOME": str(configured)})
                    self.assertEqual(1, result)
                    self.assertTrue(broken_link.is_symlink())
                    self.assertFalse(missing_target.exists())
                    self.assertFalse((fake_home / ".agents").exists())
                    self.assertFalse(install.WROTE_ANYTHING)
                    self.assertIn("symbolic link", output)
                    self.assertIn("尚未寫入任何檔案", output)


if __name__ == "__main__":
    unittest.main()


class EntryProtocolReadabilityTests(unittest.TestCase):
    """鎖住兩個實際發生過的可讀性回歸（都是模板作者看不見、裝出來才看得見的）。

    1. 佔位符寫在每一條規則上 → 替換後同一串絕對路徑重複十次，人讀不下去。
    2. 每行硬斷在 35-60 個中文字 → 句子被切成兩三截，讀的人要自己拼回去。

    這兩件事在本機檔案上完全看不出來，因為本機版沒有佔位符、也沒有被替換。
    只有把安裝結果打開才看得見——所以改成機械檢查，不靠人每次幫忙看。
    """

    def entry_block(self):
        block = install.extract_entry_protocol()
        self.assertIsNotNone(block, "規則包的 DESIGN.md 抽不出 Entry Protocol 區塊")
        return block

    def test_placeholders_declared_once_not_per_rule(self):
        block = self.entry_block()
        for marker in ("{{SKILLS_ROOT}}", "{{AGENTS_ROOT}}"):
            count = block.count(marker)
            self.assertEqual(
                count, 1,
                "{} 出現 {} 次；MUST 只在開頭宣告一次，"
                "否則替換後會變成同一串絕對路徑重複 N 遍".format(marker, count))

    def test_rules_are_not_hard_wrapped_mid_sentence(self):
        block = self.entry_block()
        offenders = [
            (i + 1, line) for i, line in enumerate(block.split("\n"))
            if line.rstrip().endswith(("，", "、", "／", "；"))
        ]
        self.assertEqual(
            offenders, [],
            "以下行結尾是句中連接符，代表句子被硬斷成多行——"
            "一條規則寫一行，讓編輯器自己 soft-wrap：{}".format(offenders))

    def test_every_installed_skill_is_reachable_from_the_entry_block(self):
        """每個被安裝的 skill，MUST 從入口文字**走得到**（可經由別的 skill 轉介）。

        直接比對「入口文字有沒有提到」是錯的斷言：debug 是 converge 的下游，
        Step 0 本來就不該直接指向它。要驗的是**傳遞可達性**——從入口文字出發，
        沿著 skill 之間的互相引用走，能不能走到每一個裝上去的 skill。
        裝了卻沒有任何路徑走得到，等於白裝。
        """
        pack_skills = Path(__file__).resolve().parent.parent / "skills"
        names = set(install.SKILLS)
        reached = {n for n in names if n in self.entry_block()}
        frontier = list(reached)
        while frontier:
            current = frontier.pop()
            skill_md = pack_skills / current / "SKILL.md"
            if not skill_md.is_file():
                continue
            text = skill_md.read_text(encoding="utf-8")
            for name in names - reached:
                if name in text:
                    reached.add(name)
                    frontier.append(name)
        unreachable = sorted(names - reached)
        self.assertEqual(
            unreachable, [],
            "從入口文字出發、沿 skill 互相引用走，走不到這些已安裝的 skill——"
            "裝了也沒有任何路徑會叫到它們：{}".format(unreachable))


class RoutingClosureTests(unittest.TestCase):
    """規則指向的 skill，MUST 全部裝得到。

    這條不是從既有寫法反推的斷言——它從**規則文字**掃出「被路由指向的
    skill 名稱」，再跟 install.py 的 SKILLS 對帳。規則新增一條指向、
    或有人把某個 skill 從 SKILLS 拿掉，兩邊任一動都會被抓到。

    實際發生過：converge 的三處路由指向 debug，而 debug 不在 SKILLS 裡，
    收件方收斂完被叫去 /debug，那個 skill 從來沒被安裝。
    """

    PACK = Path(__file__).resolve().parent.parent

    def routed_skill_names(self):
        """掃所有 SKILL.md，抓出被當成路由目的地提到的 skill 名稱。"""
        installable = set(install.SKILLS) | {install.ORCHESTRATOR}
        on_disk = {d.name for d in (self.PACK / "skills").iterdir() if d.is_dir()}
        # 只認「包裡真的有這個目錄」的名字，避免把使用環境自己的 skill
        # （feature/fix/java-dev…）誤判成本包該負責安裝的東西
        candidates = on_disk | installable
        pattern = re.compile(r"`(" + "|".join(sorted(map(re.escape, candidates))) + r")`")
        routed = set()
        for path in (self.PACK / "skills").rglob("SKILL.md"):
            text = path.read_text(encoding="utf-8")
            for name in pattern.findall(text):
                if name != path.parent.name:      # 不算自我引用
                    routed.add(name)
        return routed

    def test_every_routed_skill_is_installed(self):
        routed = self.routed_skill_names()
        missing = sorted(n for n in routed
                         if n not in set(install.SKILLS) | {install.ORCHESTRATOR})
        self.assertEqual(
            missing, [],
            "這些 skill 被規則指向、包裡也有，但 install.py 不會安裝它們——"
            "收件方照規則走會走進死巷：{}".format(missing))

    def test_every_shipped_skill_directory_is_installed(self):
        on_disk = {d.name for d in (self.PACK / "skills").iterdir() if d.is_dir()}
        installable = set(install.SKILLS) | {install.ORCHESTRATOR}
        orphans = sorted(on_disk - installable)
        self.assertEqual(
            orphans, [],
            "這些目錄在包裡但永遠不會被安裝（要嘛加進 SKILLS，要嘛從包裡移除，"
            "留著只會讓手動安裝的人裝到不該裝的東西）：{}".format(orphans))


class EntryProtocolRoutingTests(unittest.TestCase):
    """入口文字的路由必須讓進度往前走，不能把人吸回已完成的階段。

    入口文字自己寫「第一條命中就採用，不再往下看」。在那個規則下，
    條件的**順序**就是語意的一部分：如果某個一直都成立的條件
    （例如「有 docs/dev-setup.md」——做完 Phase 4 之後永遠為真）
    排在後面階段的前面，那後面的階段永遠走不到。

    實際發生過：implementation-handoff 排在 qa-handoff 之前、條件是
    「有 docs/dev-setup.md」，於是每次寫完程式回來重判都被送回去重寫，
    測試／部署／維運三個階段在字面上不可達。
    """

    PHASE_ORDER = [
        "ops-feedback",          # Phase 8，最後面的階段要最先比對
        "release-handoff",       # 7
        "qa-handoff",            # 6
        "implementation-handoff",# 5
        "system-design",         # 3
        "requirement-scoping",   # 2
    ]

    def entry_lines(self):
        block = install.extract_entry_protocol()
        self.assertIsNotNone(block, "抽不出 Entry Protocol 區塊")
        return [l for l in block.split("\n") if l.lstrip().startswith("- ")]

    def first_index(self, lines, name):
        for i, l in enumerate(lines):
            if name in l:
                return i
        self.fail("入口文字沒有任何一條規則指向 {}".format(name))

    def test_later_phases_are_matched_before_earlier_ones(self):
        lines = self.entry_lines()
        idx = [(n, self.first_index(lines, n)) for n in self.PHASE_ORDER]
        for (a, ia), (b, ib) in zip(idx, idx[1:]):
            self.assertLess(
                ia, ib,
                "{} 必須排在 {} 之前。入口文字是 first-hit-wins，"
                "把早期階段排前面會讓晚期階段永遠走不到：實際順序 {}".format(
                    a, b, [n for n, _ in sorted(idx, key=lambda t: t[1])]))

    def test_phase_five_entry_is_guarded_by_completion_state(self):
        """進 Phase 5 的條件必須帶「這個階段還沒做完」的守衛。

        沒有守衛的話，「有 docs/dev-setup.md」在整個專案生命週期都成立，
        每次回來重判都會再次命中。
        """
        lines = self.entry_lines()
        line = lines[self.first_index(lines, "implementation-handoff")]
        self.assertIn(
            "Phase 5", line,
            "進 implementation-handoff 的那一條必須引用 handoff-log 的 "
            "「## Phase 5」狀態當守衛，否則它會恆為真：{}".format(line))

    def test_in_progress_scan_comes_before_all_phase_rules(self):
        """「有分節標『進行中』就續作那一節」必須排在所有階段規則之前。"""
        lines = self.entry_lines()
        in_progress = self.first_index(lines, "狀態：進行中")
        earliest_phase = min(self.first_index(lines, n) for n in self.PHASE_ORDER)
        self.assertLess(
            in_progress, earliest_phase,
            "『狀態：進行中』的掃描必須最先做，否則做到一半的階段會被"
            "其他條件搶先命中而被跳過")


class ReinstallPreservesLocalRecordsTests(unittest.TestCase):
    """重裝不得抹掉使用者累積的框架缺陷登記。

    README 說「重複執行是安全的，之後有新版直接再跑一次就是更新」。
    但 copy_tree 是「整個目錄搬進備份再複製新的」，而登記簿跟規則放在
    同一個目錄底下——不特別保留的話，累積的紀錄會離開現行路徑，
    新的空白表就位，而使用者以為只是更新了規則。
    """

    def test_framework_defect_rows_survive_a_second_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            fake_home.mkdir(); project.mkdir()

            helper = InstallLocationTests("run_main")
            code, _ = helper.run_main(("2", str(project), "", "", ""), fake_home)
            self.assertEqual(0, code)

            registry = (project / ".claude" / "skills" / "sdlc-orchestrator"
                        / "references" / "framework-defects.md")
            self.assertTrue(registry.is_file(), "第一次安裝沒有帶出登記簿")
            marker = "| FD-01 | 我的紀錄 | x | y:1 | 矛盾 | 全部 | proposed |"
            registry.write_text(
                registry.read_text(encoding="utf-8") + "\n" + marker + "\n",
                encoding="utf-8")

            # 第二次安裝時 CLAUDE.md 已有入口區塊，會多問一次「要更新嗎」
            code, output = helper.run_main(
                ("2", str(project), "", "", "", ""), fake_home)
            self.assertEqual(0, code)
            self.assertIn(
                marker, registry.read_text(encoding="utf-8"),
                "重裝之後使用者 append 的登記列不見了——那是他為什麼改規則的"
                "唯一紀錄，比規則本身更難重建")
