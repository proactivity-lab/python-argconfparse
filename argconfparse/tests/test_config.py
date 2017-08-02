from unittest import TestCase
import os

from mock import patch

from argconfparse import argconfparse


class ConfigFileTester(TestCase):
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.conf")

    def setUp(self):
        self.parser = argconfparse.ConfigArgumentParser(
            "sample",
            description="ConfigArgumentParser test description."
        )
        self.parser.add_argument("--argument1", help="some option")
        self.parser.add_argument("--argument2", help="some other option")
        self.parser.add_argument("--argument3", help="some third option")

    def tearDown(self):
        del self.parser

    def test_config(self):
        argv = [
            "program_name",
            "-c", ConfigFileTester.CONFIG_FILE,
            "--argument1", "NOT 0123456789ABCDEF"
        ]
        with patch.object(argconfparse.argparse._sys, 'argv', argv):
            args = self.parser.parse_args()
            # precedence works
            self.assertEqual(args.argument1, 'NOT 0123456789ABCDEF')
            # conf file values work
            self.assertEqual(args.argument2, '0xFF')
            self.assertEqual(args.argument3, 't')
