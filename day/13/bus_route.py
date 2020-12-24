#!/usr/bin/env python3

import argparse

'''
Bus routes:
Your input is two lines. For example:
939
7,13,x,x,59,x,31,19

The first line is the timestamp of the earliest time you can get on the bus.

The second line is a comma separated list of bus IDs. The bus IDs also indicate the frequency of the bus.

Note that the bus arrival times are multiples of the ID:
time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .

Find the earliest bus you can take at the given timestamp, and multiply the wait time by the bus ID.
'''

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Jolts (Advent 2020 day 10')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()


'''
Wait times can be computed using <timestamp> % <id> = X, where X = minutes since the most recent bus arrival,
and <id> - X is the minutes until the next bus. The answer is the minimum <id> - X value.
'''
#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_file = open(g_args.m_file).readlines()
  l_file = [ x.rstrip() for x in l_file ]

  l_ts = int(l_file[0])
  l_routes = l_file[1].split(',')

  l_valid_routes = list()

  for l_route in l_routes:
    if l_route == 'x': continue
    l_valid_routes.append(int(l_route))

  l_min = None
  l_min_route = None

  for l_id in l_valid_routes:
    l_mod = l_ts % l_id
    l_wait_time = (l_id - l_mod) % l_id
    if l_min == None or l_wait_time < l_min:
      l_min = l_wait_time
      l_min_route = l_id

  
  print("Minimum wait time: {} minutes, route {}, product {}".format(l_min, l_min_route, l_min * l_min_route))


#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()