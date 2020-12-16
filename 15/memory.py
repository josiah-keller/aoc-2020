#!/usr/bin/env python3
"""
Implement a memory game. Seed with numbers from an input file, and then proceed
generating numbers from the age of the last number.

https://adventofcode.com/2020/day/15
"""

import argparse

class Game:
  def __init__(self, starting_numbers):
    self.numbers = starting_numbers[:]
    self.turn = len(self.numbers)
    self.seen = {}
    for i in range(len(self.numbers) - 1):
      self.seen[self.numbers[i]] = i

  def run_until(self, turn):
    while self.turn < turn:
      prev = self.numbers[-1]
      age = self.turn - 1 - self.seen.get(prev, self.turn - 1)
      self.seen[prev] = self.turn - 1
      self.numbers.append(age)
      self.turn += 1

def get_numbers(filename):
  with open(filename, 'r') as f:
    return [int(n) for n in f.read().split(',')]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file containing comma-separated starting numbers')
  args = parser.parse_args()

  numbers = get_numbers(args.filename)
  game = Game(numbers)
  game.run_until(2020)
  print(game.numbers[-1])
  game.run_until(30000000)
  print(game.numbers[-1])