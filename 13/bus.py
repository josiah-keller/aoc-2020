#!/usr/bin/env python3
"""
Given a file containing an arrival time at the bus station and a bus schedule,
figure out which bus is the earliest that can be taken.

Also, find the nifty timestamp at which each bus will arrive `i` minutes from
the timestamp when `i` is the bus's index into the schedule list.

Time is expressed as integers from a common epoch. The first line of the file
is the arrival time at the bus station. The second line is a comma-separated
list denoting the period time of each bus. Some buses are not in service, but
are denoted with an x.

https://adventofcode.com/2020/day/13
"""

import argparse

def read_schedule(filename):
  with open(filename, 'r') as f:
    arrival_time = int(f.readline().strip())
    buses = [int(period) if period != 'x' else 'x' for period in f.readline().strip().split(',')]
    return (arrival_time, buses)

def get_bus_times(arrival_time, buses):
  return [arrival_time - (arrival_time % period) + period if period != 'x' else -1 for period in buses]

def find_nifty_time(buses):
  step = 1
  t = 1
  for i in range(len(buses)):
    period = buses[i]
    if period == 'x': continue
    while (t + i) % period != 0:
      t += step
    step *= period

  return t

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file to process')
  args = parser.parse_args()

  (arrival_time, buses) = read_schedule(args.filename)
  bus_times = get_bus_times(arrival_time, buses)
  earliest_time = min([time for time in bus_times if time != -1])
  # safe to use index b/c the challenge states that there is only one correct bus
  earliest_bus = buses[bus_times.index(earliest_time)]
  print('Earliest available bus:', earliest_bus)
  print('Bus * wait time:', earliest_bus * (earliest_time - arrival_time))

  nifty_time = find_nifty_time(buses)
  print('Nifty time:', nifty_time)