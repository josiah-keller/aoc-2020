#!/usr/bin/env python3
"""
Find the three numbers in the given input file that sum to 2020. Print the
numbers and their product.

The input file's format is one number per line.
https://adventofcode.com/2020/day/1#part2
"""

import argparse

def get_input(filename):
  with open(filename, 'r') as f:
    return sorted([int(x) for x in f.readlines()])

def find_pair(numbers):
  for i in range(len(numbers)):
    for j in range(len(numbers)):
      if numbers[i] + numbers[j] >= 2020:
        continue
      for k in range(len(numbers)):
        if j == i or j == k or k == i: continue
        if numbers[i] + numbers[j] + numbers[k] == 2020:
          return (numbers[i], numbers[j], numbers[k])
  return None

def main(args):
  numbers = get_input(args.filename)
  solution = find_pair(numbers)
  print('Solution: %d, %d, %d' % solution)
  print('Product: %d' % (solution[0] * solution[1] * solution[2]))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(__doc__)
  parser.add_argument('filename', help='Path to the input file')
  args = parser.parse_args()
  main(args)