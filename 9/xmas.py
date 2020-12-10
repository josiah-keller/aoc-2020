#!/usr/bin/env python3
"""
Crack the XMAS encoding.

https://adventofcode.com/2020/day/9
"""

import argparse

def fetch_preamble(file, n):
  """
  Given a file, read the first n numbers. Sort the list for faster search.
  Return both the original list and the sorted list as a tuple.
  """
  numbers = []
  while len(numbers) < n:
    numbers.append(fetch_next(file))
  return (numbers, sorted(numbers))

def fetch_next(file):
  return int(file.readline())

def update(ls, new_number):
  """
  Given a tuple of original list and sorted list, add the new number to the
  lists and drop the oldest number. Return the updated tuple. (they are also
  updated by reference).
  """
  (numbers, sorted_numbers) = ls
  drop = numbers[0]
  numbers = numbers[1:] + [new_number]
  sorted_numbers.remove(drop) # ok for there to be duplicates b/c we just remove the first one!
  sorted_numbers.append(new_number)
  sorted_numbers.sort() # would be more efficient to iterate once and insert/remove but who cares
  return (numbers, sorted_numbers)

def is_valid(ls, number):
  """
  Given a tuple of original list and sorted list, determine whether the next
  number is valid (ie, is a sum of some pair in the list)
  """
  (numbers, sorted_numbers) = ls
  for i in range(len(sorted_numbers) - 1, 0, -1):
    if sorted_numbers[i] > number:
      continue
    for j in range(0, i):
      if sorted_numbers[i] + sorted_numbers[j] == number:
        return True

  return False

def find_range(file, target):
  """
  Given a file, read numbers to find a contiguous list of numbers that sums to
  the given target number. Return the list.
  """
  numbers = []
  candidate = sum(numbers)
  while candidate != target:
    if candidate > target:
      numbers.pop(0)
    else:
      numbers.append(fetch_next(file))
    candidate = sum(numbers)

  return numbers

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file containing XMAS data')
  parser.add_argument('--tail-len', type=int, default=25, help='Length of preamble/previous N numbers to consider')
  args = parser.parse_args()

  with open(args.filename, 'r') as f:
    tail = fetch_preamble(f, args.tail_len)
    number = fetch_next(f)
    while(is_valid(tail, number)):
      tail = update(tail, number)
      number = fetch_next(f)
    target_number = number
    print('Invalid number (target):', target_number)

    f.seek(0)
    contig = find_range(f, target_number)
    print('Found range that sums to target number:', contig)
    xmas = min(contig) + max(contig)
    print('XMAS value:', xmas)