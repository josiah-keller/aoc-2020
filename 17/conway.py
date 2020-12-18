#!/usr/bin/env python3
"""
Run a 3-or-4-D Conway game.

Input describes a 2-D plane of initial cells. From there, run the game 6 cycles
and print how many active cells there are.

https://adventofcode.com/2020/day/17
"""

import argparse

class Conway:
  ACTIVE = '#'
  def __init__(self, is_4d=False):
    self.cells = set() # set will contain a tuple of coords if that cell is active, otherwise not
    self.is_4d = is_4d

  def load_state(self, filename):
    # Initial plane will be at z=0, w=0
    # We'll interpret the first char as x=0, y=0 and increase from there
    y = 0
    with open(filename, 'r') as f:
      for line in f:
        x = 0
        for c in line:
          if c == Conway.ACTIVE:
            self.set_active((x, y, 0, 0))
          x += 1
        y += 1

  def set_active(self, coords):
    self.cells.add(coords)

  def set_inactive(self, coords):
    self.cells.discard(coords)

  def is_active(self, coords):
    return coords in self.cells

  def was_active(self, coords, state):
    return coords in state

  def get_neighbors(self, coords):
    neighbors = []
    (x, y, z, w) = coords
    for neighbor_x in range(x - 1, x + 2):
      for neighbor_y in range(y - 1, y + 2):
        for neighbor_z in range(z - 1, z + 2):
          for neighbor_w in (range(w - 1, w + 2) if self.is_4d else range(1)):
            if (neighbor_x, neighbor_y, neighbor_z, neighbor_w) == coords: continue
            neighbors.append((neighbor_x, neighbor_y, neighbor_z, neighbor_w))
    return neighbors

  def get_bounds(self):
    min_x = max_x = min_y = max_y = min_z = max_z = min_w = max_w = 0
    for coords in self.cells:
      if coords[0] < min_x:
        min_x = coords[0]
      if coords[0] > max_x:
        max_x = coords[0]
      if coords[1] < min_y:
        min_y = coords[1]
      if coords[1] > max_y:
        max_y = coords[1]
      if coords[2] < min_z:
        min_z = coords[2]
      if coords[2] > max_z:
        max_z = coords[2]
      if coords[3] < min_w:
        min_w = coords[3]
      if coords[3] > max_w:
        max_w = coords[3]
    return (
      range(min_x - 1, max_x + 2),
      range(min_y - 1, max_y + 2),
      range(min_z - 1, max_z + 2),
      range(min_w - 1, max_w + 2) if self.is_4d else range(1)
    )

  def next(self):
    (x_bounds, y_bounds, z_bounds, w_bounds) = self.get_bounds()
    old_state = self.cells.copy()

    for x in x_bounds:
      for y in y_bounds:
        for z in z_bounds:
          for w in w_bounds:
            coords = (x, y, z, w)
            neighbors = self.get_neighbors(coords)
            active_neighbors = [self.was_active(neighbor, old_state) for neighbor in neighbors].count(True)
            if self.was_active(coords, old_state):
              if active_neighbors not in (2, 3):
                self.set_inactive(coords)
            else:
              if active_neighbors == 3:
                self.set_active(coords)

  def count_active(self):
    return len(self.cells)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file containing initial state')
  parser.add_argument('--4d', dest='is_4d', action='store_true', help='Add a 4th dimension? Default is 3-D')
  args = parser.parse_args()

  conway = Conway(args.is_4d)
  conway.load_state(args.filename)
  for n in range(6):
    conway.next()

  print('Active cells:', conway.count_active())