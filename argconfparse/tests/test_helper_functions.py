from unittest import TestCase
import os

from mock import patch

from argconfparse import argconfparse


class TypeConversionTester(TestCase):
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.conf")

    def setUp(self):
        self.parser = argconfparse.ConfigArgumentParser(
            "sample",
            description="ConfigArgumentParser test description."
        )
        self.parser.add_argument(
            "--argument1",
            type=argconfparse.arg_check_hex16str,
            help="some option"
        )
        self.parser.add_argument(
            "--argument2",
            type=argconfparse.arg_hex2int,
            help="some other option"
        )
        self.parser.add_argument(
            "--argument3",
            type=argconfparse.arg_str2bool,
            help="some third option"
        )

    def tearDown(self):
        del self.parser

    def test_config_type_conversion(self):
        argv = [
            "program_name",
            "-c", TypeConversionTester.CONFIG_FILE,
        ]
        with patch.object(argconfparse.argparse._sys, 'argv', argv):
            args = self.parser.parse_args()
            self.assertEqual(args.argument1, '0123456789ABCDEF')
            self.assertEqual(args.argument2, 0xFF)
            self.assertEqual(args.argument3, True)

    def test_cmdline_type_conversion(self):
        argv = [
            "program_name",
            "-c", TypeConversionTester.CONFIG_FILE,
            "--argument1", "0011223344556677",
            "--argument2", "0x44",
            "--argument3", "f"
        ]
        with patch.object(argconfparse.argparse._sys, 'argv', argv):
            args = self.parser.parse_args()
            self.assertEqual(args.argument1, '0011223344556677')
            self.assertEqual(args.argument2, 0x44)
            self.assertFalse(args.argument3)
            self.assertIsInstance(args.argument3, bool)


class ConversionFunctionTester(TestCase):
    def test_check_hex16str(self):
        func = argconfparse.arg_check_hex16str
        self.assertRaises(ValueError, func, 'not a hex string')
        parsed = func('0123456789ABCDEF')
        self.assertEqual(parsed, '0123456789ABCDEF')

    def test_hex2str(self):
        func = argconfparse.arg_hex2int
        self.assertRaises(ValueError, func, 'not a number')
        parsed = func('0b10')
        self.assertIsInstance(parsed, int)
        self.assertEqual(parsed, 2)
        parsed = func('0x10')
        self.assertIsInstance(parsed, int)
        self.assertEqual(parsed, 16)
        parsed = func('10')
        self.assertIsInstance(parsed, int)
        self.assertEqual(parsed, 10)

    def test_str2bool(self):
        tests = [
            ('value', self.assertFalse),
            ('T', self.assertTrue),
            ('t', self.assertTrue),
            ('true', self.assertTrue),
            ('1', self.assertTrue),
            ('2', self.assertFalse),        # TODO: Should this be correct?
        ]
        for value, test_func in tests:
            parsed = argconfparse.arg_str2bool(value)
            self.assertIsInstance(parsed, bool)
            test_func(parsed)
