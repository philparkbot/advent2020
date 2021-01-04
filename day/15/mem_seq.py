#!/usr/bin/env python3

import argparse

'''
Starting sequence:
0,3,6

After starting sequence, take last number and:
* compute if it's the first occurrence
* or compute age between last two occurrences

Turn
0: 0 (starting)
1: 3 (starting)
2: 6 (starting)
3: 0 (first occurrence of 6 was turn 2)
4: 3 ("3" turn 3 - turn 0)
5: 3 ("3" turn 4 - turn 1)
6: 1 ("3" turn 5 - turn 4)
7: 0 (first occurrence of 1)
8: 4 ("0" turn 7 - turn 3)
9: 0 (first occurrence of 4)
10: 2 ("0" turn 9 - turn 7)
11: 0 (first occurrence of 2)
12: 2 ("2" turn 11 - turn 9)
13: 2 ("2" turn 12 - turn 10)
14: 1 ("2" turn 13 - turn 12)
15: 8 ("1" turn 14 - turn 6)

Note: the code for part 1 and part 2 are the same; part 2 is just a much higher stop count, so
there were modifications to allow it to keep memory usage from exploding.

'''

g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Memory sequencer (Advent 2020 day 15)')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  l_parser.add_argument('--stop', dest='m_stop', default=2020, type=int, help='Stop and print the number at the specified turn. 1 indexed.')
  g_args = l_parser.parse_args()


#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_seq = open(g_args.m_file).readlines()
  l_seq = l_seq[0].split(',')
  l_seq = [ int(x) for x in l_seq ]

  l_ledger = dict()
  l_idx = 0
  l_result = None
  l_num = None

  while l_idx < g_args.m_stop:
    if l_idx < len(l_seq):
      l_val = l_seq[l_idx]
      l_ledger[l_val] = [ l_idx ]
      if g_args.m_debug:
        print("Turn {}: initial value {}".format(l_idx+1, l_val))
    else:
      if l_num == None:
        l_num = l_seq[-1]

      assert (l_num in l_ledger), "Sanity. Could not find entry in ledger for {}. Ledger: {}".format(l_num, l_ledger)

      # if there is one occurrence, then the result is 0
      # otherwise, it's the age of the last two occurrences, so 
      l_hist = l_ledger[l_num]
      l_result = 0 if len(l_hist) == 1 else (l_hist[-1] - l_hist[-2])

      # now add the result to the ledger
      if l_result not in l_ledger: l_ledger[l_result] = list()
      l_ledger[l_result].append(l_idx)
      if len(l_ledger[l_result]) > 2:
        l_ledger[l_result] = l_ledger[l_result][-2:]
      l_num = l_result # set l_num for the next iteration

      if g_args.m_debug:
        print("Turn {}: evaluating number {}. Result={}".format(l_idx+1, l_num, l_result))

    l_idx += 1
  
  print("The number on turn {} is {}".format(g_args.m_stop, l_result))


#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()
