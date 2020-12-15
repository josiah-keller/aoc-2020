#!/usr/bin/env python3
"""
Emulate ferry docking program.

Each line of the program either sets the global "bitmask" (sort of) or
writes a value to memory at a given address.

In "v1", for every write, the "bitmask" is applied to the value before it is
written. It's really two masks. 1's are ORed in while 0's are ANDed out. Xes
pass the corresponding bit through (so they're 0's for the OR and 1's for the
AND).

In "v2", for every write, the mask is applied to the address as follows: the
0's and 1's are ORed into the address (ie, assert 1's where needed and leave
everything else). Then, each X is considered to be either value, so a number
of addresses may be written to (every combination of different X values).

Both versions are run. After each run, the sum of all values in memory
afterwards will be printed. State is reset in between runs.

https://adventofcode.com/2020/day/14
"""

import argparse

class Emulator:
  WORD_SIZE = 36

  def __init__(self, filename):
    with open(filename, 'r') as f:
      self.instructions = [self.parse_instruction(line) for line in f.readlines()]
      self.reset()

  def parse_instruction(self, line):
    """
    Parse the given line into an instruction. Instructions are tuples of
    (op, operand1, operand2). For mask instructions, operand1 is the new mask
    string and operand2 is None. For mem instructions, operand1 is the address
    and operand2 is the pre-mask value.
    """
    (lh, rh) = line.strip().replace(' ', '').split('=')
    if lh == 'mask':
      return (lh, rh, None)
    addr = int(lh.replace('mem[', '').replace(']', ''))
    value = int(rh)
    return ('mem', addr, value)

  def reset(self):
    self.memory = {}
    self.set_mask('X' * self.WORD_SIZE)

  def write_memory(self, addr, value):
    self.memory[addr] = value

  def set_mask(self, mask_str):
    self.mask_str = mask_str
    self.assert_mask = int(mask_str.replace('X', '0'), 2)
    self.clear_mask = int(mask_str.replace('X', '1'), 2)

  def mask_value(self, value):
    return (value | self.assert_mask) & self.clear_mask

  def mask_address(self, addr, mask_str=None):
    base_addr = addr | self.assert_mask
    if mask_str is None:
      mask_str = self.mask_str

    floater_idx = mask_str.find('X')
    if floater_idx == -1:
      return []

    mask = 1 << (self.WORD_SIZE - 1 - floater_idx)
    child_mask_str = mask_str[:floater_idx] + 'Z' + mask_str[floater_idx + 1:]

    addr_1 = base_addr | mask
    addr_0 = base_addr & ~mask

    return [addr_1, addr_0] + self.mask_address(addr_1, child_mask_str) + self.mask_address(addr_0, child_mask_str)

  def run_1(self):
    for (op, operand1, operand2) in self.instructions:
      if op == 'mask':
        self.set_mask(operand1)
      elif op == 'mem':
        self.write_memory(operand1, self.mask_value(operand2))

  def run_2(self):
    for (op, operand1, operand2) in self.instructions:
      if op == 'mask':
        self.set_mask(operand1)
      elif op == 'mem':
        for addr in self.mask_address(operand1):
          self.write_memory(addr, operand2)

  def sum_memory(self):
    return sum(self.memory.values())

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the file of program instructions')
  args = parser.parse_args()

  emulator = Emulator(args.filename)
  emulator.run_1()
  print('Memory sum (v1):', emulator.sum_memory())

  emulator.reset()
  emulator.run_2()
  print('Memory sum (v2):', emulator.sum_memory())