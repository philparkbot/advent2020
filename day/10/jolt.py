#!/usr/bin/env python3

import argparse
'''
Given a sequence of numbers, order them such that the difference between two numbers is less than 3.

Once that's sorted, find how many are seprated by 1, 2, or 3

Start at 0. The final value should be highest number + 3
'''

g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Jolts (Advent 2020 day 10')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_list = open(g_args.m_file).readlines()
  l_list = [ x.strip() for x in l_list ]
  l_list = [ int(x) for x in l_list ]

  l_list.sort()
  l_dist = { 0: 0, 1: 0, 2: 0, 3: 0 }

  l_prev = None
  for l_curr_jolt in l_list:
    if l_prev == None:
      l_dist[l_curr_jolt] += 1
    else:
      l_delta = l_curr_jolt - l_prev
      l_dist[l_delta] += 1

    l_prev = l_curr_jolt
  
  l_dist[3] += 1

  for l_key, l_val in l_dist.items():
    print("[{}]: {}".format(l_key, l_val))


    


#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()