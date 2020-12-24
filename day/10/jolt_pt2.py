#!/usr/bin/env python3

import argparse
'''
Given a sequence of numbers, order them such that the difference between two numbers is less than 3.

Once that's sorted, find how many are seprated by 1, 2, or 3

Start at 0. The final value should be highest number + 3


To find all the permutations, construct a delta list (a list of the deltas between successive jolts in the jolt list). Fortunately
this only contains deltas of 1 or 3. If there's a streak of 1 1 (size 2), then there are 2 possible permutations. If there's a streak of
1 1 1 (size 3), then there are 4 permutation. 1 1 1 1 (size 4) has 7 permutations. Multiply the number of permutations (based on the streak size)
together for each streak. For example, if you have a three streaks of size 4 and a streak of size 3, then the number of permutations is:
7 * 7 * 7 * 7 * 4 = 9604
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
  l_list.insert(0, 0)
  l_last_val = l_list[-1]
  l_list.append(l_last_val+3)

  l_delta_list = list()

  l_prev = None
  for l_curr_jolt in l_list:
    if l_prev != None:
      l_delta = l_curr_jolt - l_prev
      l_delta_list.append(l_delta)
    
    l_prev = l_curr_jolt
  
  print("jolt list:\n{}\ndelta list:\n{}".format(l_list, l_delta_list))

  # in the delta list, count the number of contiguous 1's
  l_delta_dist = dict()
  l_curr_streak = 0
  for l_delta in l_delta_list:
    if l_delta == 1:
      l_curr_streak += 1
    else:
      if l_curr_streak not in l_delta_dist:
        l_delta_dist[l_curr_streak] = 0
      if l_curr_streak > 0:
        l_delta_dist[l_curr_streak] += 1
      l_curr_streak = 0
  
  print("Delta breakdown:")
  for l_streak_size, l_count in l_delta_dist.items():
    print("Streak size: {}, count: {}".format(l_streak_size, l_count))




#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()