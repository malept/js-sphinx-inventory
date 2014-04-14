#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates a Sphinx inventory for MDN's JavaScript reference."""

try:
    import argcomplete
except ImportError:
    argcomplete = None
import argparse
from collections import defaultdict
import json
import logging
from sphinx_inventory import Inventory
import sys
try:
    from urllib.request import urlopen
except ImportError:
    from contextlib import closing
    import urllib2
    urlopen = lambda *a, **k: closing(urllib2.urlopen(*a, **k))
from xml.etree import cElementTree

MDN_SITEMAP = 'https://developer.mozilla.org/sitemaps/en-US/sitemap.xml'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

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


def mdn_to_refs():
    """
    Generate a cross-reference dictionary for the MDN JavaScript Reference.

    :rtype: dict
    """
    with urlopen(MDN_SITEMAP) as f:
        xml = cElementTree.parse(f)
    refs = defaultdict(dict)
    for loc in xml.iterfind('{{{ns}}}url/{{{ns}}}loc'.format(ns=SITEMAP_NS)):
        url = loc.text
        if 'JavaScript/Reference/Global_Objects/' not in url:
            continue
        url_suffix = url[81:]
        parts = url_suffix.split('/')
        if len(parts) == 1:
            name = parts[0]
            if name[0].isupper():
                ref_type = 'js:class'
            else:
                ref_type = 'js:data'
        elif len(parts) == 2:
            cls, attr = parts
            with urlopen('{url}$json'.format(url=url)) as f:
                metadata = json.load(f)
            name = '{0}.{1}'.format(cls, attr)
            if 'Method' in metadata['tags']:
                ref_type = 'js:function'
            elif 'Property' in metadata['tags']:
                ref_type = 'js:attribute'
            else:
                fmt = 'Unknown ref_type for {0}. Tags: {1}'
                log.warning(fmt.format(url, ', '.join(metadata['tags'])))
                continue
        else:
            log.warning('Skipping URL (too many parts): {0}'.format(url))
            continue
        refs[ref_type][name] = url_suffix
    return dict(refs)


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
    inv.write('js', mdn_to_refs(), args.output)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
