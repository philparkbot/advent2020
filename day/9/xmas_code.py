#!/usr/bin/env python3

import argparse

'''
* Stream of numbers.
* First N numbers (N=25 for this code) are part of the preamble.
* Every number following the preamble must be a sum of two of the N numbers prior to it

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
  l_stream = [ x.rstrip() for x in l_stream ]
  l_stream = [ int(x) for x in l_stream ]

  l_start_idx = g_args.m_preamble
  l_pass = True
  for l_idx in range(l_start_idx, len(l_stream)):
    (l_pass, l_idx1, l_idx2) = check_val(l_stream, l_idx)
    if not l_pass:
      print("Index {} (value {}) failed".format(l_idx, l_stream[l_idx]))
      break
  
  print("Code {}".format("passed" if l_pass else "failed"))

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