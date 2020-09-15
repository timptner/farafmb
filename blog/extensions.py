import re

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class InlineTableProcessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('table'):
            element.set('class', 'uk-table')


class TableExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(InlineTableProcessor(md), 'inlinetableprocessor', 15)
