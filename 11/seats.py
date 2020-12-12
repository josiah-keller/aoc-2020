#!/usr/bin/env python3
"""
Simulate the behavior of passengers on a ferry.

https://adventofcode.com/2020/day/11
"""

import argparse

class SeatSimulation:
  FLOOR = '.'
  SEAT = 'L'
  OCCUPIED = '#'

  def __init__(self, filename):
    self.neighbor_tolerance = 4
    self.load(filename)
    self.initialize_state()

  def load(self, filename):
    with open(filename, 'r') as f:
      self.layout = [[c for c in line if c != '\n'] for line in f.readlines()]

  def copy_state(self, state):
    return [row[:] for row in state]

  def initialize_state(self):
    self.state = self.copy_state(self.layout)

  def print_state(self):
    for row in self.state:
      print(''.join(row))
    print('\n')

  def run_til_settled(self):
    next_state = self.calc_next_state()
    while next_state != self.state:
      self.state = next_state
      next_state = self.calc_next_state()

  def count_occupied(self):
    return sum([row.count(SeatSimulation.OCCUPIED) for row in self.state])

  def count_occupied_neighbors(self, row_idx, seat_idx):
    count = 0
    for i in range(max(0, row_idx - 1), row_idx + 2):
      for j in range(max(0, seat_idx - 1), seat_idx + 2):
        try:
          if i == row_idx and j == seat_idx: continue
          if self.state[i][j] == SeatSimulation.OCCUPIED:
            count += 1
        except IndexError:
          pass
    return count

  def calc_next_state(self):
    new_state = self.copy_state(self.state)
    for i in range(len(self.state)):
      row = self.state[i]
      for j in range(len(row)):
        seat = row[j]
        if seat == SeatSimulation.FLOOR: continue
        if seat == SeatSimulation.SEAT:
          if self.count_occupied_neighbors(i, j) == 0:
            new_state[i][j] = SeatSimulation.OCCUPIED
        if seat == SeatSimulation.OCCUPIED:
          if self.count_occupied_neighbors(i, j) >= self.neighbor_tolerance:
            new_state[i][j] = SeatSimulation.SEAT
    return new_state

class LineOfSightSeatSimulation(SeatSimulation):
  def __init__(self, filename):
    super().__init__(filename)
    self.neighbor_tolerance = 5

  def trace_los(self, start_row, start_seat, row_delta, seat_delta):
    row = start_row + row_delta
    seat = start_seat + seat_delta
    while row >= 0 and seat >= 0 and row < len(self.state) and seat < len(self.state[row]):
      if self.state[row][seat] == SeatSimulation.OCCUPIED:
        return True
      elif self.state[row][seat] == SeatSimulation.SEAT:
        return False
      row += row_delta
      seat += seat_delta
    return False

  def count_occupied_neighbors(self, row_idx, seat_idx):
    count = 0
    for row_delta in range(-1, 2):
      for seat_delta in range(-1, 2):
        if row_delta == 0 and seat_delta == 0: continue
        if self.trace_los(row_idx, seat_idx, row_delta, seat_delta):
          count += 1

    return count

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file with the ferry seat layout')
  args = parser.parse_args()

  print('Simulation 1: tolerate up to 4 immediate neighbors')
  simulation_1 = SeatSimulation(args.filename)
  simulation_1.run_til_settled()
  print('Occupied seats:', simulation_1.count_occupied())

  print('Simulation 2: tolerate up to 5 neighbors within line of sight')
  simulation_2 = LineOfSightSeatSimulation(args.filename)
  simulation_2.run_til_settled()
  print('Occupied seats:', simulation_2.count_occupied())