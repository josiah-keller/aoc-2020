#!/usr/bin/env python3
"""
Given an input file describing a terrain map, determine how many trees the
toboggan will hit on its way down the hill for several possible slopes.

https://adventofcode.com/2020/day/3
"""

import argparse

class Terrain:
  OPEN = '.'
  TREE = '#'

  def __init__(self, filename):
    with open(filename, 'r') as f:
      self._lines = f.readlines()

    self.height = len(self._lines)
    self.width = len(self._lines[0])

  def read_coords(self, x, y):
    x = x % (self.width - 1)
    if y >= self.height:
      raise Exception('y %d out of bounds %d' % (y, self.height))

    return self._lines[y][x]

  def count_hits(self, slope_x=3, slope_y=1):
    (x, y) = (0, 0)
    trees = 0
    while y < self.height:
      obj = self.read_coords(x, y)
      if obj == Terrain.TREE:
        trees += 1
      (x, y) = (x + slope_x, y + slope_y)

    return trees

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the input file')
  args = parser.parse_args()

  terrain = Terrain(args.filename)
  slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
  ]
  product = 1
  for slope in slopes:
    hits = terrain.count_hits(*slope)
    print('(%d, %d) hits: %d' % (*slope, hits))
    product *= hits

  print('Product: %d' % product)