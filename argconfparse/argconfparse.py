""" ArgumentParser with ConfigParser thrown in."""

__author__ = "Raido Pahtma"
__license__ = "MIT"

import argparse
import ConfigParser


class ConfigArgumentParser(object):
    """ Argument parser that can take options from a configuration file. """

    def __init__(self, section, **kwargs):
        """
        @param section: Name of the application specific section to load from the configuration file.
        @param kwargs: Most regular ArgumentParser options should work and are passed on to the parser.
        """
        self.section = section

        self.conf_parser = argparse.ArgumentParser(add_help=False)
        self.conf_parser.add_argument("-c", "--conf-file", help="Specify config file", metavar="FILE")

        self.parser = argparse.ArgumentParser(parents=[self.conf_parser], **kwargs)

    def parse_args(self):
        """
        Parse command-line and configuration file arguments.
        :return: Parsed arguments.
        """
        args, remaining_argv = self.conf_parser.parse_known_args()

        if args.conf_file:
            config = ConfigParser.SafeConfigParser()

            if len(config.read([args.conf_file])) > 0:

                if config.has_section("defaults"):
                    for key, value in dict(config.items("defaults")).iteritems():
                        args, unknown = self.parser.parse_known_args(("--{}".format(key), value), namespace=args)

                if config.has_section(self.section):
                    for key, value in dict(config.items(self.section)).iteritems():
                        args, unknown = self.parser.parse_known_args(("--{}".format(key), value), namespace=args)
                        if len(unknown) > 0:
                            self.parser.error("unrecognized argument {} {}".format(key, value))

            else:
                self.parser.error("unable to read configuration file {}".format(args.conf_file))

        return self.parser.parse_args(remaining_argv, namespace=args)

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)


def arg_str2bool(v):
    """ Use this for boolean options, regular bool is always treated as True. """
    return v.lower() in ("yes", "y", "true", "t", "1")


def arg_hex2int(v):
    """ Parse integers that can be written in decimal or hex when written with 0xXXXX. """
    return int(v, 0)


def arg_check_hex16str(v):
    """ Verify that the provided argument is a 16 character hexadecimal string """
    if isinstance(v, str):
        if len(v) == 16:
            v.decode("hex")
            return v
        else:
            raise ValueError("Value must be 16 characters long")
    raise ValueError("Value must be a string")


if __name__ == '__main__':
    parser = ConfigArgumentParser("stuff", description="ConfigArgumentParser test description.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--option1", help="some option")
    parser.add_argument("--option2", help="some other option")
    parser.add_argument("--option3", help="some third option")
    args = parser.parse_args()

    print args