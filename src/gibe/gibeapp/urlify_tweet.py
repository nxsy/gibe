#!/usr/bin/env python

import re
from xml.etree import ElementTree as ET

class LastElement(object):
    def __init__(self, element, root):
        self.element = element
        self.root = root

    def append(self, text):
        if self.element is self.root:
            self.root.text = text
        else:
            self.element.tail = text

class UrlifyMatcher(object):
    RE = None
    text_name = None
    start_offset = 0

    def quote(self, value):
        from urllib import quote
        return quote(value)

    def match(self, remainder):
        if not self.RE:
            return None

        m = self.RE.search(remainder)
        if m:
            start = m.start()
            end = m.end()
            return (start, end, m, self)

    def replace(self, root, last_element, remainder, m):
        start = m.start()
        end = m.end()
        text = m.groupdict()[self.text_name]
        last_element.append(remainder[:start+self.start_offset])

        link_element = ET.SubElement(root, 'a')
        link_element.set('href', self.url_prefix + self.quote(text))
        link_element.text = text
        last_element = LastElement(link_element, root)
        remainder = remainder[end:]

        return remainder, last_element

class NicknameUrlifyMatcher(UrlifyMatcher):
    RE = re.compile(r'@(?P<nickname>\w+)')
    start_offset = 1
    text_name = "nickname"
    url_prefix = "http://twitter.com/"

class HashtagUrlifyMatcher(UrlifyMatcher):
    RE = re.compile(r'(?P<hashtag>#\w+)')
    text_name = "hashtag"
    url_prefix = "http://twitter.com/search?q="

class UrlUrlifyMatcher(UrlifyMatcher):
    RE = re.compile(r'(?P<url>https?://[^ ]+)')
    text_name = "url"
    url_prefix = ""

    def quote(self, value):
        return value

matchers = [NicknameUrlifyMatcher(), HashtagUrlifyMatcher(), UrlUrlifyMatcher()]

def urlify_tweet(tweet):
    root = ET.Element("wrapper")
    last_element = LastElement(root, root)

    remainder = tweet

    while remainder:
        earliest = None
        for matcher in matchers:
            match = matcher.match(remainder)
            if not match:
                continue
            if not earliest or match[0] < earliest[0]:
                earliest = match

        if not earliest:
            last_element.append(remainder)
            break

        start, end, m, earliest_matcher = earliest

        remainder, last_element = earliest_matcher.replace(root, last_element, remainder, m)

    return ET.tostring(root)[9:][:-10]

if __name__ == "__main__":
    import sys
    import unittest

    tests = dict(
        plain=("a", "a"),
        nick=('@nxsy', '@<a href="http://twitter.com/nxsy">nxsy</a>'),
        before_nick_after=('before @nxsy after', 'before @<a href="http://twitter.com/nxsy">nxsy</a> after'),
        hashtag=('#hashtag', '<a href="http://twitter.com/search?q=%23hashtag">#hashtag</a>'),
        before_hashtag_after=('before #hashtag after', 'before <a href="http://twitter.com/search?q=%23hashtag">#hashtag</a> after'),
        url=('http://twitter.com/', '<a href="http://twitter.com/">http://twitter.com/</a>'),
        before_url_after=('before http://twitter.com/ after', 'before <a href="http://twitter.com/">http://twitter.com/</a> after'),
        twitter_xss_incident=('http://x.xx/@"style="color:pink"onmouseover=alert(1)',
            '<a href="http://x.xx/@&quot;style=&quot;color:pink&quot;onmouseover=alert(1)">http://x.xx/@"style="color:pink"onmouseover=alert(1)</a>'),
    )

    class Tests(unittest.TestCase):
        def check(self, source, output):
            self.assertEquals(output, urlify_tweet(source))

    for k, v in tests.items():
        source, output = v
        def ch(source, output):
            return lambda self: self.check(source, output)
        setattr(Tests, 'test_' + k, ch(source, output))

    sys.argv.append("-v")
    unittest.main()
