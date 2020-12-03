#!/usr/bin/env python3
"""
Given an input file of password policy and password data pairs, print how many
of the passwords are valid according to the corresponding policy.

Each line of the input file is a password policy followed by a password
(separated by ": "). The password policy consists of two fields separated by a
space. The first field is a pair of numbers separated by a dash "-". The second
field is a character. The exact interpretation of the policy fields depends on
the selected password policy (see below).

https://adventofcode.com/2020/day/2
"""

import argparse

class UserSelectableMeta(type):
  def __str__(self):
    return self.__name__

class DefaultPasswordPolicy(metaclass=UserSelectableMeta):
  """
  Match all passwords (no-op)
  """
  @staticmethod
  def validate(entry):
    return True

  @classmethod
  def match_string(cls, policy_name):
    for subcls in cls.get_choices():
      if subcls.__name__ == policy_name:
        return subcls
    raise Exception('Unknown password policy: %s' % policy_name)

  @classmethod
  def get_choices(cls):
    return [cls] + cls.__subclasses__()

  @classmethod
  def get_choice_descriptions(cls):
    return 'POLICY DESCRIPTIONS:\n\n' + '\n\n'.join([choice.__name__ + ':\n' + choice.__doc__ for choice in cls.get_choices()])

class RangePasswordPolicy(DefaultPasswordPolicy):
  """
  Match passwords containing the specified allowable number of occurrences
  of the character.
  """
  @staticmethod
  def validate(entry):
    # in this policy, "x" and "y" are range of number of occurrences of the character
    return entry.password.count(entry.char) in range(entry.policy_x, entry.policy_y + 1)

class PositionsPasswordPolicy(DefaultPasswordPolicy):
  """
  Match passwords where, of the specified 1-based positions in the string,
  exactly one is the character.
  """
  @staticmethod
  def validate(entry):
    # in this policy, "x" and "y" are positions in the string
    return [c == entry.char for c in [entry.password[entry.policy_x - 1], entry.password[entry.policy_y - 1]]].count(True) == 1

class PasswordListEntry:
  def __init__(self, line):
    (policy, self.password) = line.split(': ')
    (rng, self.char) = policy.split(' ')
    (self.policy_x, self.policy_y) = tuple([int(x) for x in rng.split('-')])

  def is_valid(self):
    return self.policy_cls.validate(self.password)

class PasswordList:
  def __init__(self, filename, policy_cls=DefaultPasswordPolicy):
    with open(filename, 'r') as f:
      self._passwords = [PasswordListEntry(line) for line in f.readlines()]

    self.filename = filename
    self.policy_cls = policy_cls

  def count_valid(self):
    return [self.policy_cls.validate(entry) for entry in self._passwords].count(True)

def parse_password_file(filename):
  with open(filename, 'r') as f:
    return [PasswordListEntry(line) for line in f.readlines()]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__, epilog=DefaultPasswordPolicy.get_choice_descriptions(), formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('filename', help='Path to the input file to process')
  parser.add_argument('--policy', '-p', dest='policy_cls', default=DefaultPasswordPolicy, choices=DefaultPasswordPolicy.get_choices(), type=DefaultPasswordPolicy.match_string)
  args = parser.parse_args()

  password_list = PasswordList(args.filename, args.policy_cls)
  print('%d valid passwords' % password_list.count_valid())