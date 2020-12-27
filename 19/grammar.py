#!/usr/bin/env python3
"""
Validate a list of messages against a grammar.

The first section of the input file is a grammar. The second section is a list
of messages to validate. The sections are separated by a blank line.

https://adventofcode.com/2020/day/19
"""

import argparse

class Grammar:
  def __init__(self):
    self.rules = {}

  def add_rule(self, line):
    (label, expr) = line.split(':')
    if label in self.rules:
      raise Exception('Duplicate rule: %s' % label)
    self.rules[label] = expr.replace('\n', '')

  def _match_impl(self, string, rule='0'):
    if string == '':
      return (True, 0, -1)

    starting_alternation = 0

    # ugly way of communicating backtrack back up the call stack
    rule_parts = rule.split('!')
    normalized_rule = rule_parts[0]
    if len(rule_parts) == 2:
      starting_alternation = int(rule_parts[1])

    if not normalized_rule in self.rules:
      raise Exception('Unknown rule: %s' % rule)

    expr = self.rules[normalized_rule]
    alternations = expr.split('|')

    cursor = 0
    alternation_idx = 0

    while alternation_idx < len(alternations):
      alternation = alternations[alternation_idx]
      cursor = 0
      tokens = alternation.strip().split(' ')
      fail = False
      for i in range(len(tokens)):
        if alternation_idx < starting_alternation:
          # this alternation already failed earlier - we're just catching back up!
          fail = True

        token = tokens[i]
        if cursor == len(string):
          # nothing left to match - fail out
          fail = True
          break
        if token[0] == '"':
          if string[cursor] == token[1]:
            cursor += 1
          else:
            # character doesn't match - fail out
            fail = True
            break
        else:
          (match, offset, backtrack_alternation_idx) = self._match_impl(string[cursor:], token)
          cursor += offset
          if backtrack_alternation_idx > -1:
            # the child rule might still have more alternations to try in case
            # of backtracking. so we'll construct a new rule string that
            # encodes the next alternation index for the child rule and add it
            # to *our* alternations
            new_tokens = tokens[:]
            orig_token = token.split('!')[0]
            new_tokens[i] = '%s!%d' % (orig_token, backtrack_alternation_idx)
            alternations.append(' '.join(new_tokens))
          if not match:
            # child rule didn't match - fail out
            fail = True
            break

      if not fail:
        # match!
        return (True, cursor, alternation_idx + 1)

      alternation_idx += 1

    # fail
    return (False, cursor, -1)

  def match(self, string, rule='0'):
    (match, cursor, _) = self._match_impl(string, rule)
    return match and cursor == len(string)

def read_grammar(f):
  grammar = Grammar()
  line = f.readline()
  while line != '\n':
    grammar.add_rule(line)
    line = f.readline()
  return grammar

def read_inputs(f):
  inputs = []
  line = f.readline()
  while line:
    inputs.append(line.replace('\n', ''))
    line = f.readline()
  return inputs

def read_input(filename):
  with open(filename, 'r') as f:
    grammar = read_grammar(f)
    inputs = read_inputs(f)

  return (grammar, inputs)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to input file')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print list of inputs that matched')
  args = parser.parse_args()

  (grammar, inputs) = read_input(args.filename)
  matches = [grammar.match(input) for input in inputs]
  print('Matches:', matches.count(True))
  if args.verbose:
    for i in range(len(inputs)):
      if matches[i]: print(inputs[i])
