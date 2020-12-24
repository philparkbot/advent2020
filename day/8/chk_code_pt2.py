#!/usr/bin/env python3

import argparse
import re

'''
Instruction parser - detect infinite loop.

Instruction stream, start accumulator value is 0:
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

You can change one instruction, either a jmp->nop or nop->jmp, that will fix the program.

What is the final value of the accumulator of the fixed program?
'''

g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Instruction parser (Advent 2020 day 8')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()

'''
l_imap = instruction map. Track by PC/idx to detect duplicates
l_pc = program counter
'''
#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_program = open(g_args.m_file).readlines()

  for l_idx, l_instruction in enumerate(l_program):
    if 'nop' in l_instruction:
      l_program[l_idx] = re.sub('nop', 'jmp', l_program[l_idx])
    elif 'jmp' in l_instruction:
      l_program[l_idx] = re.sub('jmp', 'nop', l_program[l_idx])
    else:
      pass

    # try running code to see if it's fixed
    (l_error, l_accumulator) = run_code(l_program)

    if l_error:
      if g_args.m_debug:
        print("Loop detected. Program failed at idex {}. Accumulator is {}".format(l_idx, l_accumulator))
    else:
      print("Program passed after modifying idx {}. Accumulator is {}".format(l_idx, l_accumulator))
    
    # restore the modified instruction
    l_program[l_idx] = l_instruction


#------------------------------------------------------------------------------
def run_code(x_program):
#------------------------------------------------------------------------------
  l_end = len(x_program)
  l_imap = [ 0 for x in range(l_end) ]
  l_accumulator = 0
  l_pc = 0

  if g_args.m_debug:
    print("Program {} is length {}".format(g_args.m_file, l_end))

  l_done = False
  l_error = False

  while not l_done:
    # fetch
    l_line = x_program[l_pc]

    # check for mark instruction as touched
    if l_imap[l_pc] != 0:
      l_done = True
      l_error = True
      break
      
    l_imap[l_pc] += 1

    # decode/execute
    (l_instruction, l_val) = decode(l_line)

    if l_instruction == 'acc':
      l_accumulator += l_val

    if l_instruction == 'jmp':
      l_pc += l_val
    else:
      l_pc += 1

    l_done = l_pc >= l_end

  return (l_error, l_accumulator)


#------------------------------------------------------------------------------
def decode(x_code):
#------------------------------------------------------------------------------
  (l_instruction, l_val) = x_code.split(' ')
  l_val = int(l_val)

  return (l_instruction, l_val)

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()