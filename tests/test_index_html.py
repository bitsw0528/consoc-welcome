import os
from html.parser import HTMLParser

VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}

class TagClosingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(f"Unexpected closing tag: {tag}")
            return
        open_tag = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"Mismatched closing tag: {tag} for {open_tag}")

    def close(self):
        super().close()
        if self.stack:
            self.errors.append(f"Unclosed tags: {self.stack}")


def check_html_file(path):
    parser = TagClosingParser()
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    parser.feed(data)
    parser.close()
    return parser.errors


def test_doctype():
    with open('index.html', 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    assert first_line == '<!DOCTYPE html>'


def test_all_tags_closed():
    errors = check_html_file('index.html')
    assert not errors, 'HTML tags not properly closed: ' + '; '.join(errors)

