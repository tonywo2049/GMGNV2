import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from validate_repository import AGENTS, ROOT, validate


def load_installer():
    path = ROOT / "skills/gmgn/scripts/install_codex_agents.py"
    spec = importlib.util.spec_from_file_location("install_codex_agents", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RepositoryTests(unittest.TestCase):
    def test_contracts(self):
        validate()

    def test_installer_is_isolated_and_idempotent(self):
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"CODEX_HOME": temp_dir}):
            old_agent = Path(temp_dir) / "agents/gmgn_runner.toml"
            old_agent.parent.mkdir(parents=True)
            old_agent.write_text("v1")

            destination, installed, unchanged = installer.install()
            self.assertEqual(len(installed), len(AGENTS))
            self.assertEqual(unchanged, [])
            self.assertTrue(all(name.startswith("gmgnv2_") for name in installed))
            self.assertEqual(old_agent.read_text(), "v1")

            _, installed_again, unchanged_again = installer.install()
            self.assertEqual(installed_again, [])
            self.assertEqual(len(unchanged_again), len(AGENTS))


if __name__ == "__main__":
    unittest.main()
