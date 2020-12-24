#!/usr/bin/env python3

import argparse

'''
* Stream of numbers.
* First N numbers (N=25 for this code) are part of the preamble.
* Every number following the preamble must be a sum of two of the N numbers prior to it

Part 2:
For the invalid number you found, there is a contiguous set of numbers in the prior preamble that adds up
to the invalid number. Add the largest and smallest number of that contiguous range.
'''

g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='XMAS decoder (Advent 2020 day 9')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  l_parser.add_argument('--preamble', dest='m_preamble', default=25, type=int, help='Preamble length')
  g_args = l_parser.parse_args()


#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_stream = open(g_args.m_file).readlines()
  l_stream = [ x.rstrip() for x in l_stream ] # strip newlines
  l_stream = [ int(x) for x in l_stream ]     # convert numbers from str to int

  l_start_idx = g_args.m_preamble
  l_pass = True
  l_failing_idx = None

  for l_idx in range(l_start_idx, len(l_stream)):
    (l_pass, l_idx1, l_idx2) = check_val(l_stream, l_idx)
    if not l_pass:
      l_failing_idx = l_idx
      print("Index {} (value {}) failed".format(l_idx, l_stream[l_idx]))
      break
  
  print("Code {}".format("passed" if l_pass else "failed"))

  '''
  Now go through previous <preamble size> entries, find the contiguos range that adds up to the invalid value,
  find the min/max of that range, and print the sum
  '''
  if not l_pass:
    l_start_idx = l_failing_idx - g_args.m_preamble
    (l_found, l_first, l_last) = find_range(l_stream, 0, l_failing_idx)
    assert l_found, "No valid range found for invalid value {} at index {}".format(l_stream[l_failing_idx], l_failing_idx)
    l_min = find_min(l_stream, l_first, l_last)
    l_max = find_max(l_stream, l_first, l_last)
    if g_args.m_debug:
      print("Min is {}, max is {}, range is {}-{}, failing val is {} at idx {}".format(l_min, l_max, l_first, l_last, l_stream[l_failing_idx], l_failing_idx))
    print("value is {}".format(l_min + l_max))


#------------------------------------------------------------------------------
def find_min(x_stream, x_first, x_last):
#------------------------------------------------------------------------------
  l_min = None
  for l_idx in range(x_first, x_last+1):
    l_curr_val = x_stream[l_idx]
    l_min = l_curr_val if l_min == None or l_curr_val < l_min else l_min
  
  return l_min

#------------------------------------------------------------------------------
def find_max(x_stream, x_first, x_last):
#------------------------------------------------------------------------------
  l_max = None
  for l_idx in range(x_first, x_last+1):
    l_curr_val = x_stream[l_idx]
    l_max = l_curr_val if l_max == None or l_curr_val > l_max else l_max
  
  return l_max

'''
Find the contiguous range of numbers that add up to x_stream[x_fail_idx], starting from
x_start_idx to x_fail_idx-1. Return the first/last idx of that range.
'''
#------------------------------------------------------------------------------
def find_range(x_stream, x_start_idx, x_fail_idx):
#------------------------------------------------------------------------------
  l_first_idx = x_start_idx
  l_target_val = x_stream[x_fail_idx]
  l_found = False

  l_final_start_idx = None
  l_final_end_idx = None

  if g_args.m_debug:
    print("Starting search for contiguous range to add up to {}, starting at idx {} to {}".format(l_target_val, x_start_idx, x_fail_idx-1))

  while l_first_idx < x_fail_idx and not l_found:
    l_last_idx = l_first_idx + 1

    while l_last_idx < x_fail_idx and not l_found:
      l_curr_val = sum_range(x_stream, l_first_idx, l_last_idx)
      if l_curr_val == l_target_val:
        l_found = True
        l_final_start_idx = l_first_idx
        l_final_end_idx = l_last_idx
        break
      elif l_curr_val < l_target_val:
        pass
      else:
        break

      l_last_idx += 1
    l_first_idx += 1

  return (l_found, l_final_start_idx, l_final_end_idx)

'''
Sum numbers between start/end, inclusive
'''
#------------------------------------------------------------------------------
def sum_range(x_stream, x_start, x_end):
#------------------------------------------------------------------------------
  l_sum = 0
  assert (x_start < x_end), "start index {} smaller than end idx {}".format(x_start, x_end)

  for l_idx in range(x_start, x_end + 1):
    l_sum += x_stream[l_idx]
  
  return l_sum

'''
Check the XMAS encoding stream to see if the number specified at the index is valid
'''
#------------------------------------------------------------------------------
def check_val(x_stream, x_idx):
#------------------------------------------------------------------------------
  l_num = x_stream[x_idx]
  l_pass = False
  l_start_idx = x_idx - g_args.m_preamble

  for l_idx1 in range(l_start_idx, x_idx - 1):
    for l_idx2 in range(l_idx1 + 1, x_idx):
      l_pass = (x_stream[l_idx1] + x_stream[l_idx2] == l_num)
      if g_args.m_debug:
        print("Checking {}+{} ([{}]+[{}]) = {} (pass={})".format(x_stream[l_idx1], x_stream[l_idx2], l_idx1, l_idx2, l_num, l_pass))
      if l_pass:
        return (l_pass, l_idx1, l_idx2)
  
  return (l_pass, None, None)

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()