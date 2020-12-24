#!/usr/bin/env python3

import argparse

'''
Bus routes:
Your input is two lines. For example:
939
7,13,x,x,59,x,31,19

Part 2:
The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute. (The first line in your input is no longer relevant.)

For example, suppose you have the same list of bus IDs as above:

7,13,x,x,59,x,31,19

An x in the schedule means there are no constraints on what bus IDs must depart at that time.

This means you are looking for the earliest timestamp (called t) such that:

    Bus ID 7 departs at timestamp t.
    Bus ID 13 departs one minute after timestamp t.
    There are no requirements or restrictions on departures at two or three minutes after timestamp t.
    Bus ID 59 departs four minutes after timestamp t.
    There are no requirements or restrictions on departures at five minutes after timestamp t.
    Bus ID 31 departs six minutes after timestamp t.
    Bus ID 19 departs seven minutes after timestamp t.

The only bus departures that matter are the listed bus IDs at their specific offsets from t. Those bus IDs can depart at other times, and other bus IDs can depart at those times. For example, in the list above, because bus ID 19 must depart seven minutes after the timestamp at which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes after timestamp t.

In this example, the earliest timestamp at which this occurs is 1068781:

time     bus 7   bus 13  bus 59  bus 31  bus 19
1068773    .       .       .       .       .
1068774    D       .       .       .       .
1068775    .       .       .       .       .
1068776    .       .       .       .       .
1068777    .       .       .       .       .
1068778    .       .       .       .       .
1068779    .       .       .       .       .
1068780    .       .       .       .       .
1068781    D       .       .       .       .
1068782    .       D       .       .       .
1068783    .       .       .       .       .
1068784    .       .       .       .       .
1068785    .       .       D       .       .
1068786    .       .       .       .       .
1068787    .       .       .       D       .
1068788    D       .       .       .       D
1068789    .       .       .       .       .
1068790    .       .       .       .       .
1068791    .       .       .       .       .
1068792    .       .       .       .       .
1068793    .       .       .       .       .
1068794    .       .       .       .       .
1068795    D       D       .       .       .
1068796    .       .       .       .       .
1068797    .       .       .       .       .

Here are some other examples:

    The earliest timestamp that matches the list 17,x,13,19 is 3417.
    67,7,59,61 first occurs at timestamp 754018.
    67,x,7,59,61 first occurs at timestamp 779210.
    67,7,x,59,61 first occurs at timestamp 1261476.
    1789,37,47,1889 first occurs at timestamp 1202161486.



'''

g_iter = 10
g_args = None

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Bus routes (Advent 2020 day 13')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()


'''
Essentially:
Find t such that:
(t + offset) % id == 0
for all offsets

Fastest way to find the solution would be to sort by id, and increment by largest id.
Is there a faster way for very large lists aside from multithreading??

Yes: Chinese remainder theorem. See pt3.
'''
#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_file = open(g_args.m_file).readlines()
  l_file = [ x.rstrip() for x in l_file ]
  l_routes = l_file[1].split(',')

  '''
  l_id_map[route id] = index (offset) in route list input
  '''
  l_id_map = dict()

  for l_idx, l_route in enumerate(l_routes):
    if l_route == 'x': continue
    l_route = int(l_route)
    l_id_map[l_route] = l_idx
  
  l_largest = sorted(l_id_map.keys(), reverse=True)[0]
  l_t = l_id_map[l_largest] * -1
  l_done = False
  l_iter = 0

  if g_args.m_debug:
    print("Largest route id is {} at offset {}".format(l_largest, l_id_map[l_largest]))

  while not l_done:
    l_done = True
    l_t += l_largest
    l_iter += 1

    if g_args.m_debug:
      if tapered_print(l_iter):
        print("Iteration {}: trying t={}".format(l_iter, l_t), flush=True)

    for l_route in sorted(l_id_map.keys(), reverse=True):
      l_idx = l_id_map[l_route]

      if (l_t + l_idx) % l_route != 0:
        l_done = False
        break

  print("The timestamp is {}".format(l_t))
  

'''
Print frequently at first, and less frequently as the number of iterations increase
'''
#------------------------------------------------------------------------------
def tapered_print(x_iter):
#------------------------------------------------------------------------------
  global g_iter

  l_mod = 0

  if x_iter < g_iter:
    l_mod = g_iter / 100
  else:
    g_iter *= 10
    l_mod = g_iter / 100

  
  l_print = x_iter < 10 or (x_iter % l_mod == 0)
  return l_print



#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()