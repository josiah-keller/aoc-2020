#!/usr/bin/env python3
"""
Process rules specifying what types of bags may be contained by other bags.
Two modes are supported.

ancestor mode: determine the number of types of bags that may contain a shiny
gold bag.

children mode: determine the number of bags required inside one shiny gold bag.

Each line of the file is a rule. Each rule maps a bag type to a list of other
bag types prefixed by quantities. I was going to actually write out a grammar
for it here, but... nah.

https://adventofcode.com/2020/day/7
"""

import argparse, re

BAG_PATTERN = re.compile(r'bags?')

class LuggageRule:
  index = {}
  def __init__(self, line, ruleset):
    self.ruleset = ruleset

    (bag_type, contents) = line.split('contain')
    self.type = re.sub(BAG_PATTERN, '', bag_type).strip()

    unbagged_contents_list = [
      re.sub(BAG_PATTERN, '', s).replace('.', '').strip() for s in contents.split(',')
    ]
    self.contents_list = []
    for contents in unbagged_contents_list:
      (qty_str, bag_type) = contents.split(' ', 1)
      if qty_str == 'no':
        break
      self.contents_list.append({
        'qty': int(qty_str),
        'bag_type': bag_type
      })

    if self.type in self.ruleset.index:
      raise Exception('Duplicate rule for "%s"' % self.type)
    self.ruleset.index[self.type] = self

  def can_contain(self, target_type):
    return any([
      contents['bag_type'] == target_type
      or (contents['bag_type'] in self.ruleset.index
        and self.ruleset.index[contents['bag_type']].can_contain(target_type)
      )
      for contents in self.contents_list])

class LuggageRules:
  def __init__(self, filename):
    self.index = {}
    with open(filename, 'r') as f:
      self.rules = [LuggageRule(line, self) for line in f.readlines()]

  def count_ancestors(self, target_type):
    return [rule.can_contain(target_type) for rule in self.rules].count(True)

  def count_children(self, target_type):
    rule = self.index.get(target_type)
    if rule is None:
      raise Exception('No rule for "%s"' % target_type)

    return sum([
      contents['qty'] + contents['qty'] * self.count_children(contents['bag_type'])
      for contents in rule.contents_list
    ])

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file containing rules')
  parser.add_argument('--mode', choices=['ancestor', 'children'], required=True, help='Count ancestors of the shiny gold bag? Or count children?')
  args = parser.parse_args()

  rules = LuggageRules(args.filename)
  if args.mode == 'ancestor':
    print('%d bags can contain a shiny gold bag' % rules.count_ancestors('shiny gold'))
  elif args.mode == 'children':
    print('A shiny gold bag contains %d other bags' % rules.count_children('shiny gold'))