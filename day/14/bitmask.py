#!/usr/bin/env python3

import argparse
import re

'''
Given this input:
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0

Each memory location applies the mask before writing the value to memory. X means don't care (preserve the existing value),
and 0/1 mean overwrite the bit in that position to 0/1.

Apply the mask to each memory location, and report the sum of all memory locations.
'''

g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Bitmask (Advent 2020 day 14)')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_input = open(g_args.m_file).readlines()
  l_input = [ x.rstrip() for x in l_input ]

  l_mem = dict()
  l_and_mask = None
  l_or_mask = None

  for l_line in l_input:
    if 'mask' in l_line:
      l_match = re.search('mask = ([X01]+)', l_line)
      assert l_match, "Sanity - no mask found"
      l_mask = l_match.group(1)

      l_and_mask = re.sub('X', '1', l_mask)
      l_or_mask = re.sub('X', '0', l_mask)

      l_and_mask = int(l_and_mask, 2)
      l_or_mask = int(l_or_mask, 2)
    else:
      l_match = re.search("mem\[(\d+)\] = (\d+)", l_line)
      assert l_match, "Sanity - no match found for line {}".format(l_line)
      (l_addr, l_val) = l_match.group(1, 2)
      l_addr = int(l_addr)
      l_val = int(l_val)

      l_final_val = (l_val & l_and_mask) | l_or_mask
      l_mem[l_addr] = l_final_val

  # count memory
  l_sum = 0
  for l_addr in l_mem.keys():
    l_sum += l_mem[l_addr]
  
  print("Sum is {} ({})".format(l_sum, hex(l_sum)))








#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()
