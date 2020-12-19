#!/usr/bin/env python3
"""
Evaluate math expressions without order of operations. Input file can contain
an expression on each line.

https://adventofcode.com/2020/day/18
"""

import argparse

# approximate grammars implemented here:
#
# part 1:
# LINE : EXPR\n
# EXPR : TERM (OPERATOR TERM)*
# TERM : NUMBER|(EXPR)
#
# part 2:
# LINE : EXPR\n
# EXPR : FACTOR (\* FACTOR)*
# FACTOR : TERM (\+ TERM)*
# TERM : NUMBER|\(EXPR\)

class Token:
  def __init__(self, tok_type, token):
    self.type = tok_type
    self.token = token

  def __str__(self):
    return '[%s] %s' % (self.type, self.token)

class LexError(Exception):
  pass

class Lexer:
  def __init__(self, line):
    self.line = line
    self.cursor = 0
    self.next()

  def next(self):
    self.lookahead = self.get_next()

  def get_next(self):
    try:
      t = self.line[self.cursor]
      token = []
      while t in (' ', '\t'):
        self.cursor += 1
        t = self.line[self.cursor]

      if t.isnumeric():
        while t.isnumeric():
          token.append(t)
          self.cursor += 1
          t = self.line[self.cursor]
        return Token('NUMBER', ''.join(token))

      if t in ('+', '*', '(', ')', '\n'):
        self.cursor += 1
        return Token(t, t)

      raise LexError('Illegal character "%s"' % t)
    except IndexError:
      return Token(None, None)

class ParseError(Exception):
  pass

class Parser:
  def __init__(self, line):
    self.lexer = Lexer(line)

  def expect(self, t):
    if not self.match(t):
      raise ParseError('Expected %d, got "%d" instead' % (t, self.lexer.lookahead.type))

  def match(self, t):
    if t == self.lexer.lookahead.type:
      self.lexer.next()
      return True
    return False

  def peek(self, t):
    return t == self.lexer.lookahead.type

  def consume(self):
    t = self.lexer.lookahead.token
    self.lexer.next()
    return t

  def parse_line(self):
    return self.parse_expression()

  def parse_factor(self):
    value = self.parse_term()
    while self.match('+'):
      rh = self.parse_term()
      value += rh
    return value

  def parse_term(self):
    if self.peek('NUMBER'):
      return int(self.consume())
    elif self.match('('):
      value = self.parse_expression()
      self.expect(')')
      return value
    else:
      raise ParseError('Expected NUMBER or (EXPR), got "%s" instead' % self.lexer.lookahead.type)

class FlatParser(Parser):
  def parse_expression(self):
    value = self.parse_term()
    while self.peek('+') or self.peek('*'):
      operation = self.consume()
      rh = self.parse_term()
      if operation == '+':
        value += rh
      elif operation == '*':
        value *= rh
    return value

class AddFirstParser(Parser):
  def parse_expression(self):
    value = self.parse_factor()
    while self.match('*'):
      rh = self.parse_factor()
      value *= rh
    return value

def evaluate(line, parser_cls):
  parser = parser_cls(line)
  return parser.parse_line()

def do_hw(filename, mode):
  if mode == 'flat':
    parser_cls = FlatParser
  elif mode == 'addfirst':
    parser_cls = AddFirstParser
  with open(filename, 'r') as f:
    values = [evaluate(line, parser_cls) for line in f]
    print(sum(values))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Input file with expressions to evaluate')
  parser.add_argument('mode', choices=['flat', 'addfirst'], help='Order of operations mode')
  args = parser.parse_args()

  do_hw(args.filename, args.mode)