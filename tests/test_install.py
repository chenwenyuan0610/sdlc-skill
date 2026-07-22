import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import install


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
            if skill != "change-request":
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

    def test_storage_custom_path_is_asked_only_for_choice_three(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            custom = project / "my-skills"
            for choice in (1, 2):
                with self.subTest(choice=choice), \
                        mock.patch.object(install, "ask_choice", return_value=choice), \
                        mock.patch.object(install, "ask_path") as ask_path:
                    install.choose_storage_root(
                        "skills", "project", "claude", project)
                    ask_path.assert_not_called()
            with mock.patch.object(install, "ask_choice", return_value=3), \
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

    def test_main_project_agents_can_override_to_claude_storage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            fake_home.mkdir()
            project.mkdir()
            result, _ = self.run_main(
                ("2", str(project), "2", "2", "2"), fake_home)

            self.assertEqual(0, result)
            skills_root = project / ".claude" / "skills"
            self.assertTrue((skills_root / "qa-handoff" / "SKILL.md").is_file())
            self.assertFalse((project / ".agents").exists())
            self.assertIn(
                str(skills_root),
                (project / "AGENTS.md").read_text(encoding="utf-8"),
            )

    def test_main_can_mix_skill_and_agent_standard_roots(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            fake_home = sandbox / "home"
            project = sandbox / "project"
            fake_home.mkdir()
            project.mkdir()
            result, _ = self.run_main(
                ("2", str(project), "2", "2", ""), fake_home)

            skills_root = project / ".claude" / "skills"
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
                ("2", str(project), "2", "3", str(custom_skills), "yes", ""),
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
                 "3", str(custom_skills), "yes",
                 "3", str(custom_agents), "yes"),
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
                ("", "", "3", str(custom_skills), "yes", ""),
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
                "phase-exit": (Path("skills") / install.SKILLS[0] /
                               "references" / "phase-exit-criteria.md"),
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
