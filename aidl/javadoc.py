# Copyright (c) 2013 Christopher Thunes

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import re

def join(s):
    return ' '.join(l.strip() for l in s.split('\n'))

class DocBlock(object):
    def __init__(self):
        self.description = ''
        self.return_doc = None
        self.params = []

        self.authors = []
        self.deprecated = False

        # @exception and @throw are equivalent
        self.throws = {}
        self.exceptions = self.throws

        self.tags = {}

    def add_block(self, name, value):
        value = value.strip()

        if name == 'param':
            try:
                param, description = value.split(None, 1)
            except ValueError:
                param, description = value, ''
            self.params.append((param, join(description)))

        elif name in ('throws', 'exception'):
            try:
                ex, description = value.split(None, 1)
            except ValueError:
                ex, description = value, ''
            self.throws[ex] = join(description)

        elif name == 'return':
            self.return_doc = value

        elif name == 'author':
            self.authors.append(value)

        elif name == 'deprecated':
            self.deprecated = True

        self.tags.setdefault(name, []).append(value)

blocks_re = re.compile('(^@)', re.MULTILINE)
leading_space_re = re.compile(r'^\s*\*', re.MULTILINE)
blocks_justify_re = re.compile(r'^\s*@', re.MULTILINE)

def _sanitize(s):
    s = s.strip()

    if not (s[:3] == '/**' and s[-2:] == '*/'):
        raise ValueError('not a valid Javadoc comment')

    s = s.replace('\t', '    ')

    return s

def _uncomment(s):
    # Remove /** and */
    s = s[3:-2].strip()

    return leading_space_re.sub('', s)

def _get_indent_level(s):
    return len(s) - len(s.lstrip())

def _left_justify(s):
    lines = s.rstrip().splitlines()

    if not lines:
        return ''

    indent_levels = []
    for line in lines:
        if line.strip():
            indent_levels.append(_get_indent_level(line))
    indent_levels.sort()

    common_indent = indent_levels[0]
    if common_indent == 0:
        return s
    else:
        lines = [line[common_indent:] for line in lines]
        return '\n'.join(lines)

def _force_blocks_left(s):
    return blocks_justify_re.sub('@', s)

def parse(raw):
    sanitized = _sanitize(raw)
    uncommented = _uncomment(sanitized)
    justified = _left_justify(uncommented)
    justified_fixed = _force_blocks_left(justified)
    prepared = justified_fixed

    blocks = blocks_re.split(prepared)

    doc = DocBlock()

    if blocks[0] != '@':
        doc.description = blocks[0].strip()
        blocks = blocks[2::2]
    else:
        blocks = blocks[1::2]

    for block in blocks:
        try:
            tag, value = block.split(None, 1)
        except ValueError:
            tag, value = block, ''

        doc.add_block(tag, value)

    return doc
