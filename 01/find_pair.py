#!/usr/bin/env python3
"""
Find the pair of numbers in the given input file that sums to 2020. Print the
numbers and their product.

The input file's format is one number per line.
https://adventofcode.com/2020/day/1
"""

import argparse

def get_input(filename):
  with open(filename, 'r') as f:
    return [int(x) for x in f.readlines()]

def find_pair(numbers):
  for i in range(len(numbers)):
    for j in range(len(numbers)):
      if j == i: continue
      if numbers[i] + numbers[j] == 2020:
        return (numbers[i], numbers[j])
  return None

def main(args):
  numbers = get_input(args.filename)
  pair = find_pair(numbers)
  print('Pair: %d, %d' % pair)
  print('Product: %d' % (pair[0] * pair[1]))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(__doc__)
  parser.add_argument('filename', help='Path to the input file')
  args = parser.parse_args()
  main(args)