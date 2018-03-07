import unittest
from unittest import TestCase

from app.video import Video


class TestVideo(TestCase):
    def setUp(self):
        pass

    def test_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            Video("nonexistent_file.mp4")

    def test_ConfigFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            Video("nonexistent_file.mp4", "nonexistent_file.ini")


if __name__ == '__main__':
    unittest.main()
