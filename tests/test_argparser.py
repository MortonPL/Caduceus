from argparse import ArgumentError
import unittest
from unittest.mock import patch
import sys

from src.config import Config

class TestArgParser(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config()

    def test_target(self):
        args = ['', 'sometarget', 'dir1']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1'], 'config': None}
            self.config.parse_args()
            self.assertDictEqual(self.config, expected)

    def test_no_args(self):
        args = ['']
        with patch.object(sys, 'argv', args):
            with patch.object(self.config.__parser__, 'exit_on_error', False):
                self.assertRaises(ArgumentError)

    def test_dirs(self):
        args = ['', 'sometarget', 'dir1', 'dir2', 'dir3']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1', 'dir2', 'dir3'], 'config': None}
            self.config.parse_args()
            self.assertDictEqual(self.config, expected)

    def test_config(self):
        args = ['', 'sometarget', 'dir1', '-c', 'abba.conf']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1'], 'config': 'abba.conf'}
            self.config.parse_args()
            self.assertDictEqual(self.config, expected)

        args = ['', 'sometarget', 'dir1', '--config', 'abba.conf']
        with patch.object(sys, 'argv', args):
            expected = {'target':'sometarget', 'directories': ['dir1'], 'config': 'abba.conf'}
            self.config.parse_args()
            self.assertDictEqual(self.config, expected)

if __name__ == "__main__":
    unittest.main()
