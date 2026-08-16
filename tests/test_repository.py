from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from validate_repository import AGENTS, ROOT, validate


def load_script(name):
    path = ROOT / f"skills/gmgn/scripts/{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RepositoryTests(unittest.TestCase):
    def test_contracts(self):
        validate()

    def test_installer_is_isolated_and_idempotent(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            old_agent = Path(temp_dir) / "agents/gmgn_runner.toml"
            old_agent.parent.mkdir(parents=True)
            old_agent.write_text("v1")

            destination, installed, unchanged, removed = installer.sync()
            self.assertEqual(len(installed), len(AGENTS))
            self.assertEqual(unchanged, [])
            self.assertEqual(removed, [])
            self.assertTrue((destination / installer.STATE_FILE).is_file())
            self.assertEqual(installer.check()[1], [])
            self.assertEqual(old_agent.read_text(), "v1")

            _, installed_again, unchanged_again, removed_again = installer.sync()
            self.assertEqual(installed_again, [])
            self.assertEqual(len(unchanged_again), len(AGENTS))
            self.assertEqual(removed_again, [])

    def test_hook_mode_reports_only_when_profiles_change(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(installer.main(["sync", "--hook"]), 0)
            self.assertEqual(json.loads(output.getvalue())["hookSpecificOutput"]["hookEventName"], "SessionStart")

            customized = Path(temp_dir) / "agents/gmgnv2_runner.toml"
            customized.write_bytes(customized.read_bytes() + b"\n# user customization\n")
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(installer.main(["sync", "--hook"]), 0)
            self.assertEqual(output.getvalue(), "")
            self.assertTrue(customized.read_bytes().endswith(b"# user customization\n"))

    def test_installer_check_rejects_invalid_installed_toml(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            destination, installed, _, _ = installer.sync()
            (destination / installed[0]).write_text("invalid = [")

            self.assertTrue(installer.check()[1])

    def test_installer_removes_stale_managed_profiles(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            destination, _, _, _ = installer.sync()
            stale = destination / "gmgnv2_retired.toml"
            stale.write_text("retired")
            state_path = destination / installer.STATE_FILE
            state = json.loads(state_path.read_text())
            state["files"][stale.name] = installer.digest(stale.read_bytes())
            state_path.write_text(json.dumps(state))

            with patch.object(installer, "plugin_version", return_value="next-version"):
                _, _, _, removed = installer.sync()
            self.assertEqual(removed, [stale.name])
            self.assertFalse(stale.exists())

    def test_installer_preserves_customization_until_new_version(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            old_agent = Path(temp_dir) / "agents/gmgn_runner.toml"
            old_agent.parent.mkdir(parents=True)
            old_agent.write_text("v1")
            destination, installed, _, _ = installer.sync()
            customized = destination / installed[0]
            original = customized.read_bytes()
            customized.write_bytes(original + b"\n# user customization\n")

            self.assertEqual(installer.sync()[1], [])
            self.assertEqual(installer.check()[1], [])
            self.assertNotEqual(customized.read_bytes(), original)

            with patch.object(installer, "plugin_version", return_value="next-version"):
                self.assertIn(customized.name, installer.sync()[1])
            self.assertEqual(customized.read_bytes(), original)

            _, removed, preserved = installer.uninstall()
            self.assertEqual(len(removed), len(AGENTS))
            self.assertEqual(preserved, [])
            self.assertEqual(old_agent.read_text(), "v1")
            self.assertFalse((destination / installer.STATE_FILE).exists())

    def test_uninstall_preserves_untracked_named_profile(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            profile = Path(temp_dir) / "agents/gmgnv2_runner.toml"
            profile.parent.mkdir(parents=True)
            profile.write_text("user-owned")

            installer.uninstall()

            self.assertEqual(profile.read_text(), "user-owned")

    def test_uninstall_preserves_modified_managed_profile(self):
        installer = load_script("install_codex_agents")
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            destination, installed, _, _ = installer.sync()
            profile = destination / installed[0]
            profile.write_bytes(profile.read_bytes() + b"\n# user customization\n")

            installer.uninstall()

            self.assertTrue(profile.is_file())

    def test_plugin_install_syncs_and_checks_the_installed_copy(self):
        manager = load_script("manage_codex_install")
        with tempfile.TemporaryDirectory() as temp_dir:
            plugin_root = Path(temp_dir)
            installer = plugin_root / "skills/gmgn/scripts/install_codex_agents.py"
            installer.parent.mkdir(parents=True)
            installer.write_text("")
            commands = []

            with patch.object(manager, "run_json", return_value={"installedPath": temp_dir}), patch.object(
                manager, "run", side_effect=lambda command: commands.append(command) or ""
            ):
                self.assertEqual(manager.install_plugin(), plugin_root)

            self.assertEqual(commands[-2][-1], "sync")
            self.assertEqual(commands[-1][-1], "check")

    def test_marketplace_update_uses_the_matching_source_flow(self):
        manager = load_script("manage_codex_install")
        with patch.object(manager, "run_json") as run_json:
            manager.update_marketplace({"marketplaceSource": {"sourceType": "git"}})
            run_json.assert_called_once_with(
                ["codex", "plugin", "marketplace", "upgrade", manager.MARKETPLACE, "--json"]
            )

        commands = []
        with patch.object(manager, "run", side_effect=lambda command: commands.append(command) or ""):
            manager.update_marketplace({
                "root": "/tmp/gmgn-v2-source",
                "marketplaceSource": {"sourceType": "local"},
            })
        self.assertEqual(commands[-1][-2:], ["pull", "--ff-only"])


if __name__ == "__main__":
    unittest.main()
