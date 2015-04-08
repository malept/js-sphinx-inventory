# -*- coding: utf-8 -*-

try:
    from urllib.request import urlopen
except ImportError:
    from contextlib import closing
    import urllib2
    urlopen = lambda *a, **k: closing(urllib2.urlopen(*a, **k))

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

__all__ = ['ElementTree', 'urlopen']
