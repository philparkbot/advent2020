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

Steps:
Find t such that:
(t + offset) % id == 0
for all offsets

Chinese remainder theorem:
For the first example (17,x,13,19):
1. t % 17 == 0
2. (t + 2) % 13 == 0
3. (t + 3) % 19 == 0

Rewritten:
1. t % 17 == 0
2. t % 13 == 13 - 2 = 11
3. t % 19 == 19 - 3 = 16

b1, b2, b3 = remainders
n1, n2, n3 = mods
N = n1*n2*n3
N1 = n2*n3
N2 = n1*n3
N3 = n2*n3
x1, x2, x3 = inverses

b1=0
b2=11
b3=16

n1=17
n2=13
n3=19

N1=13*19=247
N2=17*19=323
N3=13*17=221

N=13*17*19=4199

To solve for inverses (x1, x2, x3):
x1: N1*x1 % n1 == 1
x2: N2*x2 % n2 == 1
x3: N3*x3 % n3 == 1

x1:
247*x1 % 17 = 1
9*x1 % 17 = 1
x1 = 2

x2:
323*x2 % 13 = 1
11*x2 % 13 = 1
x2 = 6

x3:
221*x3 % 19 = 1
12*x3 % 19 = 1
x3 = 8

x = sum(bi*Ni*xi)
= 0*247*2 + 11*323*6 + 19*221*8
= 21318 + 28288
= 49606
49606 % N
= 49606 % 4199
= 3417

In code form:
1. b1, b2, b3 = remainder = mod - offset
2. n1, n2, n3 = mod (route)
3. N=n1*n2*n3
  a. N1 = N/n1
  b. N2 = N/n2
  ...
4. Compute inverses x1, x2, x3...
  a. N1*x1 % n1 = 1
  b. N2*x2 % n2 = 1
  ...
5. x = sum(bi*Ni*xi)
6. Answer = x % N
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


#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_file = open(g_args.m_file).readlines()
  l_file = [ x.rstrip() for x in l_file ]
  l_routes = l_file[1].split(',')

  '''
  l_id_map[offset]['remainder'] = remainder = mod - offset
  l_id_map[offset]['mod'] = mod (route)
  l_id_map[offset]['Ni'] = N / l_id_map[offset]['mod'] (compute N first)
  l_id_map[offset]['inverse'] = inverse
  '''
  l_id_map = dict()

  for l_idx, l_route in enumerate(l_routes):
    if l_route == 'x': continue
    l_route = int(l_route)
    l_id_map[l_idx] = dict()
    l_id_map[l_idx]['remainder'] = l_route - l_idx
    l_id_map[l_idx]['mod'] = l_route

  # compute N
  l_N = 1
  for l_offset in l_id_map.keys():
    l_N *= l_id_map[l_offset]['mod']
  
  # Set Ni and compute inverses
  for l_offset in l_id_map.keys():
    l_id_map[l_offset]['Ni'] = int(l_N / l_id_map[l_offset]['mod'])
    l_inverse = compute_inverse(l_id_map[l_offset]['Ni'], l_id_map[l_offset]['mod'])
    l_id_map[l_offset]['inverse'] = l_inverse

  l_x = 0
  for l_offset in l_id_map.keys():
    l_x += (l_id_map[l_offset]['remainder'] * l_id_map[l_offset]['Ni'] * l_id_map[l_offset]['inverse'])

  l_t = l_x % l_N
  print("The timestamp is {}".format(l_t))
  
'''
Given x_N * x % x_mod == 1, solve for x. Just brute force it, because fuck it.
'''
#------------------------------------------------------------------------------
def compute_inverse(x_N, x_mod):
#------------------------------------------------------------------------------
  l_x = None
  l_found = False

  for l_val in range(10000):
    if (l_val * x_N) % x_mod == 1:
      l_found = True
      l_x = l_val
      break

  assert l_found, "No inverse value found"
  return l_x


#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()