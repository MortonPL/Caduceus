from argparse import ArgumentError
import unittest
from unittest.mock import patch
import sys

from src.argparser import ArgParser

class TestArgParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = ArgParser()

    def test_target(self):
        args = ['', 'sometarget', 'dir1']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1']}
            self.assertDictEqual(self.parser.parse(), expected)

    def test_no_args(self):
        args = ['']
        with patch.object(sys, 'argv', args):
            with patch.object(self.parser.__parser__, 'exit_on_error', False):
                self.assertRaises(ArgumentError)

    def test_dirs(self):
        args = ['', 'sometarget', 'dir1', 'dir2', 'dir3']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1', 'dir2', 'dir3']}
            self.assertDictEqual(self.parser.parse(), expected)

if __name__ == "__main__":
    unittest.main()
