#!/usr/bin/env python3
"""
Process an input file of airline seat information. The seat information
is encoded in a binary format, with B or R being 1 and F or L being 0.

https://adventofcode.com/2020/day/5
"""

import argparse

SEAT_TO_INT = str.maketrans('BRFL', '1100')

def parse_seats(filename):
  with open(filename, 'r') as f:
    return sorted([int(line.translate(SEAT_TO_INT), 2) for line in f.readlines()])

def find_seat(seats):
  for i in range(1, len(seats) - 1):
    if seats[i] - seats[i-1] > 1:
      return seats[i] - 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file to process')
  args = parser.parse_args()

  seats = parse_seats(args.filename)
  max_id = seats[-1]
  print('Max seat id: %d' % max_id)
  print('Our seat: %d' % find_seat(seats))