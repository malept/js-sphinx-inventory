# -*- coding: utf-8 -*-

from collections import defaultdict
import html5lib
from ._compat import urlopen

HTML_NS = html5lib.constants.namespaces['html']


def tag(name):
    return '{{{ns}}}{name}'.format(ns=HTML_NS, name=name)

TAG_DIV = tag('div')
TAG_A = tag('a')
LINK_XPATH = './{li}/{a}'.format(li=tag('li'), a=TAG_A)
sig_xpath = lambda href: './/{p}[@id="{href}"]/{code}'.format(p=tag('p'),
                                                              code=tag('code'),
                                                              href=href)


def element_matches(element, tag, cls):
    return element.tag == tag and element.get('class') == cls


def add_to_refs(refs, rtype, cls, attr, identifier):
    if attr:
        ref_name = '{cls}.{attr}'.format(cls=cls, attr=attr)
    else:
        ref_name = cls
    if not cls.startswith('Backbone'):
        ref_name = 'Backbone.{0}'.format(ref_name)
    refs[rtype][ref_name] = identifier


def parse_io(file_like_object):
    refs = defaultdict(dict)
    doc = html5lib.parse(file_like_object)
    sidebar = doc.find('.//{tag}[@id="sidebar"]'.format(tag=TAG_DIV))
    body = doc.find('.//{tag}[@class="container"]'.format(tag=TAG_DIV))
    for child in sidebar:
        if element_matches(child, TAG_A, 'toc_title'):
            href = child.get('href')
            if len(href) > 1 and href[1].isupper():
                title = child.text.strip()
                if title in ('Sync', 'Utility'):
                    continue
                add_to_refs(refs, 'class', title, None, child.get('href'))
            else:
                title = None
        elif element_matches(child, tag('ul'), 'toc_section'):
            if title is None:
                continue
            for link in child.findall(LINK_XPATH):
                href = link.get('href')
                if not link.text:
                    continue
                cls = title
                if link.text.startswith('Backbone.'):
                    cls, attr = link.text.split('.', 1)
                elif link.text == 'constructor / initialize':
                    for attr in link.text.split(' / '):
                        add_to_refs(refs, 'function', cls, attr, href)
                    continue
                else:
                    attr = link.text.split(' ')[0]
                rtype = 'attribute'
                sig = body.find(sig_xpath(href[1:]))
                if sig is not None and '(' in sig.text:
                    rtype = 'function'
                add_to_refs(refs, rtype, cls, attr, href)
    return dict(refs)


def parse():
    """Generate a cross-reference dictionary for Backbone.js."""
    with urlopen('http://backbonejs.org/') as f:
        return parse_io(f)
