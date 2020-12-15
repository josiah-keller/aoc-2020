#!/usr/bin/env python3
"""
Given an input file of password records, validate the records. By default,
merely check for the presence of required fields. Optionally, also validate
each field's value against additional, stricter rules.

https://adventofcode.com/2020/day/4
"""

import argparse, re

YEAR_PATTERN = re.compile(r'^\d{4}$')
HCL_PATTERN = re.compile(r'^#[0-9a-f]{6}$')
EYE_COLORS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
PID_PATTERN = re.compile(r'^\d{9}$')

class PasswordRecord:
  DEFAULT_VALIDATION_RULES = {
    'byr': lambda _: True,
    'iyr': lambda _: True,
    'eyr': lambda _: True,
    'hgt': lambda _: True,
    'hcl': lambda _: True,
    'ecl': lambda _: True,
    'pid': lambda _: True
  }

  STRICT_VALIDATION_RULES = {
    'byr': lambda byr: YEAR_PATTERN.match(byr) is not None and int(byr) in range(1920, 2002 + 1),
    'iyr': lambda iyr: YEAR_PATTERN.match(iyr) is not None and int(iyr) in range(2010, 2020 + 1),
    'eyr': lambda eyr: YEAR_PATTERN.match(eyr) is not None and int(eyr) in range(2020, 2030 + 1),
    'hgt': lambda hgt: ('cm' in hgt and int(hgt.replace('cm', '')) in range(150, 193 + 1)) \
      or ('in' in hgt and int(hgt.replace('in', '')) in range(59, 76 + 1)),
    'hcl': lambda hcl: HCL_PATTERN.match(hcl) is not None,
    'ecl': lambda ecl: ecl in EYE_COLORS,
    'pid': lambda pid: PID_PATTERN.match(pid) is not None
  }

  def __init__(self, data=None):
    self._fields = {}
    if data is not None:
      self.add_data(data)

  def add_data(self, data):
    fields = data.split(' ')
    for field in fields:
      (key, value) = field.split(':')
      self._fields[key] = value

  def get_field(self, key):
    return self._fields.get(key, None)

  def has_field(self, key):
    return key in self._fields

  def is_valid(self, rules=None):
    if rules is None:
      rules = PasswordRecord.DEFAULT_VALIDATION_RULES
    return all([self.has_field(key) and rules[key](self.get_field(key)) for key in rules])

  def is_empty(self):
    return len(self._fields) == 0

class PassportRecordsList:
  def __init__(self, filename):
    with open(filename, 'r') as f:
      self._records = self.read_file(f)

  def read_file(self, f):
    records = []
    record = PasswordRecord()
    for line in f:
      if line == '\n':
        records.append(record)
        record = PasswordRecord()
        continue
      record.add_data(line.replace('\n', ''))

    if not record.is_empty():
      records.append(record)

    return records

  def count_valid(self, rules=None):
    return [record.is_valid(rules) for record in self._records].count(True)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the input file to validate')
  parser.add_argument('--strict', action='store_true', help='Use "strict" validation rules')
  args = parser.parse_args()

  rules = PasswordRecord.STRICT_VALIDATION_RULES if args.strict else PasswordRecord.DEFAULT_VALIDATION_RULES
  records = PassportRecordsList(args.filename)
  print('Valid records: %d' % records.count_valid(rules))