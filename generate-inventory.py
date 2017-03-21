#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates a Sphinx inventory for MDN's JavaScript reference."""

try:
    import argcomplete
except ImportError:
    argcomplete = None
import argparse
import logging
from sphinx_inventory import Inventory
from sphinx_inventory.js import mdn
import sys

if sys.version_info >= (3,):
    from functools import partial
    open = partial(open, encoding='utf-8')

log = logging.getLogger(__name__)


def parse_args(prog, args):
    """
    Define and parse arguments for the script.

    :param str prog: The name of the script
    :param list args: The arguments to process
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(prog, description=__doc__)
    parser.add_argument('output', metavar='FILENAME', help='Output filename')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')
    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser.parse_args(args)


def configure_logger(level):
    """
    Configure the logger.

    :param int level: The log level for the handler.
    """
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    log.addHandler(handler)


def main(argv):
    """
    CLI runner.

    :type argv: list
    :return: shell return code (0 for success, nonzero otherwise)
    :rtype: int
    """
    args = parse_args(argv[0], argv[1:])
    if args.verbose:
        level = logging.INFO
    else:
        level = logging.ERROR
    configure_logger(level)

    inv = Inventory(b'MDN JavaScript Reference', b'1.0')
    inv.write('js', mdn.parse(), args.output)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
