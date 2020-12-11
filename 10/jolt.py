#!/usr/bin/env python3
"""
Follow the chain of joltage adapters and count the different joltage gaps
between each adapter.

https://adventofcode.com/2020/day/10
"""

import argparse

def read_joltages(filename):
  with open(filename, 'r') as f:
    return sorted([int(line) for line in f.readlines()])

def jolt_stats(joltages):
  gaps = { 1: 0, 2: 0, 3: 0 }
  prev = 0 # first joltage is 0
  variant_counts = [1] + [0] * joltages[-1]
  for joltage in joltages:
    gap = joltage - prev
    if gap not in gaps:
      raise Exception('Invalid joltage gap!')
    gaps[gap] += 1
    variant_counts[joltage] = sum([variant_counts[joltage - step] for step in range(1, 4)])
    prev = joltage

  # last joltage is +3
  gaps[3] += 1

  return {
    'gaps': gaps,
    'variants': variant_counts[-1]
  }

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file of joltage adapter info')
  args = parser.parse_args()

  joltages = read_joltages(args.filename)
  stats = jolt_stats(joltages)
  gaps = stats['gaps']
  print('1-gaps:', gaps[1], '2-gaps:', gaps[2], '3-gaps:', gaps[3])
  print('1-gaps * 3-gaps:', gaps[1] * gaps[3])
  print('Variants:', stats['variants'])
