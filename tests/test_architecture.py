import ast
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]


class ArchitectureTests(unittest.TestCase):
    def test_dependency_boundaries(self):
        forbidden = {
            "backend": {"frontend", "application", "tkinter", "customtkinter", "PIL"},
            "frontend": {
                "backend",
                "application",
                "sqlite3",
                "requests",
                "gdown",
                "py7zr",
                "subprocess",
                "threading",
                "webbrowser",
            },
            "application": {"backend", "frontend", "tkinter", "customtkinter", "PIL", "sqlite3"},
            "contracts": {
                "backend",
                "frontend",
                "application",
                "tkinter",
                "customtkinter",
                "sqlite3",
            },
        }
        for layer, denied in forbidden.items():
            for path in (PROJECT / layer).rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    names = (
                        [alias.name for alias in node.names]
                        if isinstance(node, ast.Import)
                        else ([node.module or ""] if isinstance(node, ast.ImportFrom) else [])
                    )
                    for name in names:
                        self.assertNotIn(
                            name.split(".")[0],
                            denied,
                            f"{path.relative_to(PROJECT)} imports {name}",
                        )

    def test_backend_runs_without_gui_and_third_party_packages(self):
        with tempfile.TemporaryDirectory() as home:
            script = """
import importlib.abc, sys
class DenyGui(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name.split('.')[0] in {'frontend', 'tkinter', 'customtkinter', 'PIL'}:
            raise AssertionError('GUI import: ' + name)
sys.meta_path.insert(0, DenyGui())
from backend.api import LauncherService
service = LauncherService()
service.initialize()
assert service.list_games() == ()
assert service.scores() == {}
assert service.platform('ps2').id == 'ps2'
print('headless-ok')
"""
            result = subprocess.run(
                [sys.executable, "-S", "-c", script],
                cwd=PROJECT,
                env=dict(os.environ, RASPBERRY_LAUNCHER_HOME=home, DISPLAY=""),
                text=True,
                capture_output=True,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("headless-ok", result.stdout)

    def test_importing_frontend_opens_no_window_and_loads_no_backend(self):
        try:
            import customtkinter  # noqa: F401
        except ImportError:
            self.skipTest("Instale requirements/frontend.txt para verificar o frontend.")
        script = """
import tkinter, sys
import frontend.window, frontend.preview
assert tkinter._default_root is None
assert not any(name == 'backend' or name.startswith('backend.') for name in sys.modules)
print('frontend-independent')
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=PROJECT,
            env=dict(os.environ, DISPLAY=""),
            text=True,
            capture_output=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("frontend-independent", result.stdout)
