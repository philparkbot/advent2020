#!/usr/bin/env python3

import argparse
import copy
import re

'''
Given this input:
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0

Part 2:
The mask is applied to the mem address, and the maks is now bitwise OR, with X | (0|1) = X.

After applying the mask, expand the X to cover all permutations of 0/1 and write the value to mem.
The answer is the sum of all values in mem (any values not explicity written default to 0).
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

  l_mask = None
  l_mem = dict()
  l_addr_array = list()

  for l_line in l_input:
    if 'mask' in l_line:
      l_match = re.search('mask = ([X01]+)', l_line)
      assert l_match, "Sanity - no mask found"
      l_mask = l_match.group(1)
      l_addr_array = list()

    else:
      l_match = re.search("mem\[(\d+)\] = (\d+)", l_line)
      assert l_match, "Sanity - no match found for line {}".format(l_line)
      (l_orig_addr, l_val) = l_match.group(1, 2)
      l_val = int(l_val)
      l_addr = format(int(l_orig_addr), 'b').zfill(len(l_mask))

      l_masked_addr = bitwise_or(l_mask, l_addr)
      expand_X(l_masked_addr, l_addr_array)

      if g_args.m_debug:
        print("Addr {} (bin {}), mask:{}, masked addr: {}, expands to {}".format(l_orig_addr, bin(int(l_orig_addr)), l_mask, "".join(l_masked_addr), [ hex(x) for x in l_addr_array ]))

      # now write to all addresses in array
      for l_addr in l_addr_array:
        l_mem[l_addr] = l_val

        if g_args.m_debug:
          print("Writing mem[{}]={}".format(bin(l_addr), l_val))
        #print("Writing mem[{}]={}".format(hex(l_addr), l_val))
      
      # clear address array
      l_addr_array = list()
  
  if g_args.m_debug:
    print("Memory dump:")
    for l_addr, l_val in l_mem.items():
      print("mem[{}]={}".format(hex(l_addr), l_val))

  l_sum = 0
  for l_offset, l_val in l_mem.items():
    l_sum += l_val
  
  print("Answer is {}".format(l_sum))

# The only thing different with a regular bitwise OR is support for X.
# Return a list of the OR'd bits.
#------------------------------------------------------------------------------
def bitwise_or(x_mask, x_addr):
#------------------------------------------------------------------------------
  assert len(x_mask) == len(x_addr), "length mismatch"

  l_masked_addr = list()
  for l_pos in range(len(x_mask)):
    l_final_val = None
    if x_mask[l_pos] == 'X' or x_mask[l_pos] == '1':
      l_final_val = x_mask[l_pos]
    else:
      l_final_val = x_addr[l_pos]
    l_masked_addr.append(l_final_val)
    #if g_args.m_debug:
    #  print("mask[{}]={}, addr[{}]={}, final={}".format(l_pos, x_mask[l_pos], l_pos, x_addr[l_pos], l_final_val))

  
  return l_masked_addr
 
#------------------------------------------------------------------------------
def expand_X(x_val, x_list):
#------------------------------------------------------------------------------
  l_val = copy.deepcopy(x_val)

  for l_pos, l_bit in enumerate(l_val):
    if l_bit == 'X':
      l_copy = copy.deepcopy(l_val)
      l_val[l_pos] = '0'
      l_copy[l_pos] = '1'
      expand_X(l_copy, x_list)
  
  assert ('X' not in l_val), "Sanity"
  l_int = int("".join(l_val), 2)
  x_list.append(l_int)


#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()