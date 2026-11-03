# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import rm


class RemovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_directory_requires_explicit_recursion(self):
        folder = self.root / "folder"
        folder.mkdir()
        file = folder / "keep"
        file.write_text("keep")
        self.assertEqual(rm.main([str(folder)]), 1)
        self.assertTrue(file.exists())

    def test_recursive_removal_does_not_follow_symlinks(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "keep").write_text("keep")
        folder = self.root / "folder"
        folder.mkdir()
        (folder / "link").symlink_to(outside, target_is_directory=True)
        self.assertEqual(rm.main(["-r", str(folder)]), 0)
        self.assertTrue((outside / "keep").exists())

    def test_broken_symlink_is_removed(self):
        link = self.root / "broken"
        link.symlink_to(self.root / "missing")
        self.assertEqual(rm.main([str(link)]), 0)
        self.assertFalse(link.is_symlink())

    def test_interactive_refusal_preserves_file(self):
        file = self.root / "keep"
        file.write_text("keep")
        with patch("builtins.input", return_value="n"):
            self.assertEqual(rm.main(["-i", str(file)]), 0)
        self.assertTrue(file.exists())

    def test_empty_directory_flag(self):
        folder = self.root / "empty"
        folder.mkdir()
        self.assertEqual(rm.main(["-d", str(folder)]), 0)
        self.assertFalse(folder.exists())

    def test_missing_and_force(self):
        self.assertEqual(rm.main([str(self.root / "missing")]), 1)
        self.assertEqual(rm.main(["-f", str(self.root / "missing")]), 0)
        self.assertEqual(rm.main(["-f"]), 0)

    def test_protected_paths_are_rejected_before_traversal(self):
        with patch.object(Path, "iterdir", side_effect=AssertionError("must not traverse")):
            for name in ("/", ".", ".."):
                with self.assertRaises(OSError):
                    rm.remove(name, recursive=True, force=True)


if __name__ == "__main__":
    unittest.main()
