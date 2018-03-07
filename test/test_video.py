import unittest
from unittest import TestCase

from app.video import Video


class TestVideo(TestCase):
    def setUp(self):
        pass

    def test_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            Video("nonexistent_file.mp4")


if __name__ == '__main__':
    unittest.main()
