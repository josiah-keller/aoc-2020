#!/usr/bin/env python3
"""
Interpret fictional game system bootloader code.

https://adventofcode.com/2020/day/8
"""

import argparse

class Interpreter:
  CONTINUE = 0
  LOOP = 1
  HALT = 2
  valid_instructions = frozenset(['acc', 'jmp', 'nop'])

  def __init__(self, filename=None):
    if filename is not None:
      self.load(filename)

  def load(self, filename):
    with open(filename, 'r') as f:
      self.instructions = [self.parse(line) for line in f.readlines()]

  def parse(self, line):
    (opcode, operand) = line.split(' ', 1)
    if opcode not in Interpreter.valid_instructions:
      raise Exception('Invalid instruction: %s' % opcode)
    try:
      operand = int(operand)
    except:
      operand = 0
    return (opcode, operand)

  def reset(self):
    self.visited = set()
    self.accumulator = 0
    self.pc = 0

  def exec(self):
    status = self.next()
    while status == Interpreter.CONTINUE:
      status = self.next()
    return status

  def next(self):
    if self.pc in self.visited:
      return Interpreter.LOOP
    if self.pc >= len(self.instructions):
      return Interpreter.HALT
    self.visited.add(self.pc)
    (opcode, operand) = self.instructions[self.pc]
    self.dispatch_instruction(opcode, operand)
    return Interpreter.CONTINUE

  def dispatch_instruction(self, opcode, operand):
    getattr(self, 'inst_%s' % opcode)(operand)

  def set_pc(self, new_pc):
    self.pc = new_pc

  def inst_acc(self, operand):
    self.accumulator += operand
    self.set_pc(self.pc + 1)

  def inst_jmp(self, operand):
    self.set_pc(self.pc + operand)

  def inst_nop(self, operand):
    self.set_pc(self.pc + 1)

  def does_halt(self):
    return self.exec() == Interpreter.HALT

  def find_halt(self):
    """
    Find a jmp or nop that, when toggled to the other op, allows the program to
    halt. Return the pc of that instruction, or -1 if the program already halts
    """
    self.reset()
    if self.does_halt():
      return -1
    for pc in range(len(self.instructions)):
      (opcode, operand) = self.instructions[pc]
      # We're interested in trying any jmp, but only nops that wouldn't become self-jmps
      if opcode == 'jmp' or (opcode == 'nop' and operand != 0):
        self.instructions[pc] = ('nop' if opcode == 'jmp' else 'jmp', operand)
        self.reset()
        if self.does_halt():
          return pc
        self.instructions[pc] = (opcode, operand)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('filename', help='Path to the code file')
  parser.add_argument('--mode', choices=['find_loop', 'find_halt'], required=True, help='Find first loop? or find first halt?')
  args = parser.parse_args()

  interpreter = Interpreter(args.filename)

  if args.mode == 'find_loop':
    interpreter.reset()
    exit_code = interpreter.exec()
    if exit_code != Interpreter.LOOP:
      print('Halted without looping')
    else:
      print('Accumulator before loop: %d' % interpreter.accumulator)
  elif args.mode == 'find_halt':
    fixed_pc = interpreter.find_halt()
    if fixed_pc == -1:
      print('Already halts')
    else:
      print('Changed instruction %d (%s %d) to allow halt' % (fixed_pc, *interpreter.instructions[fixed_pc]))
    print('Accumulator at halt: %d' % interpreter.accumulator)