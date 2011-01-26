#!/usr/bin/python

import markdown
import re

SHEBANG_COLON_RE = re.compile(r'''
    (?:(?:::+)|(?P<shebang>[#]!))       # Shebang or 2 or more colons.
    (?P<path>(?:/\w+)*[/ ])?        # Zero or 1 path 
    (?P<lang>[\w+-]*)               # The language 
    ''',  re.VERBOSE)

class SyntaxHighlighterTreeprocessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        blocks = root.getiterator('pre')
        for block in blocks:
            children = block.getchildren()
            if len(children) != 1:
                continue
            if children[0].tag != 'code':
                continue

            text = children[0].text
            lines = text.split("\n")
            first_line = lines.pop(0)

            m = SHEBANG_COLON_RE.search(first_line)
            if m:
                try:
                    self.lang = m.group('lang').lower()
                except IndexError:
                    self.lang = None
                if m.group('path'):
                    # path exists - restore first line
                    lines.insert(0, first_line)

                if self.lang:
                    children[0].text = "\n".join(lines).strip("\n")
                    block.text = "\n".join(lines).strip("\n")
                    block.set('class', 'brush: python')
                    block.remove(children[0])

class SyntaxHighlighterExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        syntaxhighlighter = SyntaxHighlighterTreeprocessor(md)
        md.treeprocessors.add("syntaxhighlighter", syntaxhighlighter, "_end") 

def makeExtension():
  return SyntaxHighlighterExtension()
