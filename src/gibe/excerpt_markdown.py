#!/usr/bin/env python

import re

import markdown

class ExcerptExtension(markdown.Extension):
    excerpt_content = ""

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('excerpt_block', 
             ExcerptBlockProcessor(md.parser), 
             "_begin")

        md.treeprocessors.add("excerpt", ExcerptTreeprocessor(md), ">inline")

class ExcerptBlockProcessor(markdown.blockprocessors.BlockProcessor):
    RE = re.compile(r'(^|\n)[ ]{0,3}(?P<excerpt_type>(hidden)?excerpt)>[ ]?(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        tag = m.groupdict()['excerpt_type']
        if m:
            before = block[:m.start()]

            # Pass lines before excerpt in recursively for parsing forst.
            self.parser.parseBlocks(parent, [before])

            # Remove ``excerpt> `` from begining of each line.
            block = '\n'.join([self.clean(line, tag) for line in
                            block[m.start():].split('\n')])
        sibling = self.lastChild(parent)
        if sibling and sibling.tag == tag:
            # Previous block was a excerpt so set that as this blocks parent
            quote = sibling
        else:
            # This is a new excerpt. Create a new parent element.
            quote = markdown.etree.SubElement(parent, tag)
        # Recursively parse block with excerpt as parent.
        self.parser.parseChunk(quote, block)

    def clean(self, line, excerpt_type):
        """ Remove ``>`` from beginning of a line. """
        m = self.RE.match(line)
        if line.strip() == "%s>" % (excerpt_type,):
            return ""
        elif m:
            return m.group(2)
        else:
            return line

class ExcerptTreeprocessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        excerpt = root.find('excerpt')
        if excerpt:
            self.markdown.excerpt = excerpt

        parent_map = dict((c, p) for p in root.getiterator() for c in p if c.tag == "hiddenexcerpt")
        if parent_map:
            for child, parent in parent_map.items():
                child.tag = "div"
                self.markdown.excerpt = child
                parent.remove(child)
