# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import logging
from .compat import ElementTree, urlopen

MDN_SITEMAP = 'https://developer.mozilla.org/sitemaps/en-US/sitemap.xml'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

log = logging.getLogger(__name__)


def parse():
    """
    Generate a cross-reference dictionary for the MDN JavaScript Reference.

    :rtype: dict
    """
    with urlopen(MDN_SITEMAP) as f:
        xml = ElementTree.parse(f)
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
                ref_type = 'class'
            else:
                ref_type = 'data'
        elif len(parts) == 2:
            cls, attr = parts
            with urlopen('{url}$json'.format(url=url)) as f:
                metadata = json.loads(f.read().decode('utf-8'))
            name = '{0}.{1}'.format(cls, attr)
            if 'Method' in metadata['tags']:
                ref_type = 'function'
            elif 'Property' in metadata['tags']:
                ref_type = 'attribute'
            else:
                fmt = 'Unknown ref_type for {0}. Tags: {1}'
                log.warning(fmt.format(url, ', '.join(metadata['tags'])))
                continue
        else:
            log.warning('Skipping URL (too many parts): {0}'.format(url))
            continue
        refs[ref_type][name] = url_suffix
    return dict(refs)
