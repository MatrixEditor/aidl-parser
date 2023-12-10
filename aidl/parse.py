# Copyright (c) 2013 Christopher Thunes
# Modified 2023 by MatrixEditor

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
from __future__ import annotations

from aidl.parser import Parser
from aidl.tokenizer import tokenize
from aidl.tree import Declaration, Expression, Type, CompilationUnit

def parse_expression(exp: str) -> Expression:
    if not exp.endswith(';'):
        exp = exp + ';'

    tokens = tokenize(exp)
    parser = Parser(tokens)

    return parser.parse_expression()

def parse_member_signature(sig: str) -> Declaration:
    if not sig.endswith(';'):
        sig = sig + ';'

    tokens = tokenize(sig)
    parser = Parser(tokens)

    return parser.parse_member_declaration()

def parse_constructor_signature(sig: str) -> Declaration:
    # Add an empty body to the signature, replacing a ; if necessary
    if sig.endswith(';'):
        sig = sig[:-1]
    sig = sig + '{ }'

    tokens = tokenize(sig)
    parser = Parser(tokens)

    return parser.parse_member_declaration()

def parse_type(string: str) -> Type:
    tokens = tokenize(string)
    parser = Parser(tokens)

    return parser.parse_type()

def parse_type_signature(sig: str) -> Declaration:
    if sig.endswith(';'):
        sig = sig[:-1]
    sig = sig + '{ }'

    tokens = tokenize(sig)
    parser = Parser(tokens)

    return parser.parse_class_or_interface_declaration()

def fromstring(s: str | bytes) -> CompilationUnit:
    tokens = tokenize(s)
    parser = Parser(tokens)
    return parser.parse()
