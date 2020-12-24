#!/usr/bin/env python3

import argparse
import re

'''
The input string contains directions for ship movement:
N/S/E/W/F<num>

or:
R/L<num>

For N/S/E/W/F, you move <num> units in that direction. F is forward, so you move
forward <num> units. N/S/E/W do not change which direction you're facing.

For R/L<num>, you turn R/L <num> degrees (in increments of 90 degrees) which changes
the current direction you're facing.

Decode the directions and find the ending Manhattan coordinates.
'''

g_args = None
g_compass = [ 'N', 'E', 'S', 'W' ]

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
  # current coordinates = (<current direction>, <x>, <y>)
  l_current_coordinates = ('E', 0, 0)
  '''
  N: +y
  S: -y
  E: +x
  W: -x
  '''

  for l_line in open(g_args.m_file).readlines():
    l_line = l_line.rstrip()
    l_match = re.search("(\w)(\d+)", l_line)
    assert l_match, "Sanity: no match"

    (l_cmd, l_val) = l_match.group(1, 2)
    l_val = int(l_val)
    l_current_coordinates = execute(l_cmd, l_val, l_current_coordinates)

  (l_dir, l_x, l_y) = l_current_coordinates
  l_dist = abs(l_x) + abs(l_y)
  print("Final coordinates ({}, {}, {}) (distance={})".format(l_dir, l_x, l_y, l_dist))

#------------------------------------------------------------------------------
def execute(x_cmd, x_val, x_coordinates):
#------------------------------------------------------------------------------
  (l_dir, l_x, l_y) = x_coordinates

  if x_cmd == 'F':
    x_cmd = l_dir

  if x_cmd == 'N':
    l_y += x_val
  elif x_cmd == 'S':
    l_y -= x_val
  elif x_cmd == 'E':
    l_x += x_val
  elif x_cmd == 'W':
    l_x -= x_val
  elif x_cmd == 'L' or x_cmd == 'R':
    assert x_val % 90 == 0, "Invalid value for {}{}".format(x_cmd, x_val)
    # don't need this
    # if x_val >= 360: x_val = x_val / 360
    l_units = int(x_val / 90)
    l_idx = g_compass.index(l_dir)
    if x_cmd == 'L':
      l_idx -= l_units
    else:
      l_idx += l_units

    if l_idx > 3: l_idx = l_idx % 4
    l_dir = g_compass[l_idx]

  else:
    assert 0, "Sanity, invalid cmd {}".format(l_cmd)

  return (l_dir, l_x, l_y)

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()