#!/usr/bin/env python3

import argparse
import re

'''
The input string contains directions for ship movement:
N/S/E/W/F<num>

or:
R/L<num>

Part 2: there is now a waypoint that is set relative to the ship.

N/S/E/W means move the waypoint by <num> units.

L/R moves the waypoint clockwise/counterclockwise around the ship.

F means move the ship forward to the waypoint <num>*<distance>, where <distance>
is the relative distance to the waypoint.

If the ship moves, the waypoint also moves.

Decode the directions and find the ending Manhattan coordinates.

I don't remember my complex number math, but it looks like multiplying coordinates by -j is equivalent to a 90 CW rotation,
and multiplying by j is equivalent to a 90 CCW rotation.
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
  # ship coordinates = (<x>, <y>)
  l_ship_coordinates = complex(0, 0)
  l_waypoint_coordinates = complex(10, 1)

  '''
  N: +y
  S: -y
  E: +x
  W: -x
  '''

  if g_args.m_debug:
      print("initial ship coordinates:({}, {}), waypoint:({}, {})".format(int(l_ship_coordinates.real), int(l_ship_coordinates.imag), int(l_waypoint_coordinates.real), int(l_waypoint_coordinates.imag)))

  for l_line in open(g_args.m_file).readlines():
    l_line = l_line.rstrip()
    l_match = re.search("(\w)(\d+)", l_line)
    assert l_match, "Sanity: no match"

    (l_cmd, l_val) = l_match.group(1, 2)
    l_val = int(l_val)
    (l_ship_coordinates, l_waypoint_coordinates) = execute(l_cmd, l_val, l_ship_coordinates, l_waypoint_coordinates)

    if g_args.m_debug:
      print("cmd:{}{}, new ship coordinates:({}, {}), waypoint:({}, {})".format(l_cmd, l_val, int(l_ship_coordinates.real), int(l_ship_coordinates.imag), int(l_waypoint_coordinates.real), int(l_waypoint_coordinates.imag)))

  l_dist = abs(int(l_ship_coordinates.real)) + abs(int(l_ship_coordinates.imag))
  print("Final coordinates ({}, {}) (distance={})".format(int(l_ship_coordinates.real), int(l_ship_coordinates.imag), l_dist))

#------------------------------------------------------------------------------
def execute(x_cmd, x_val, x_ship, x_waypoint):
#------------------------------------------------------------------------------
  # relative coordinates of the waypoint to the ship
  l_delta = x_waypoint - x_ship
  
  if x_cmd == 'N':
    x_waypoint += complex(0, x_val)
  elif x_cmd == 'S':
    x_waypoint -= complex(0, x_val)
  elif x_cmd == 'E':
    x_waypoint += complex(x_val, 0)
  elif x_cmd == 'W':
    x_waypoint -= complex(x_val, 0)
  elif x_cmd == 'L' or x_cmd == 'R':
    assert x_val % 90 == 0, "Invalid value for {}{}".format(x_cmd, x_val)
    # don't need this
    # if x_val >= 360: x_val = x_val / 360
    l_units = int(x_val / 90)

    if x_cmd == 'R':
      for l_count in range(l_units):
        l_delta *= complex(0, -1)
    else:
      for l_count in range(l_units):
        l_delta *= complex(0, 1)
    
    x_waypoint = x_ship + l_delta

  elif x_cmd == 'F':
    l_move = l_delta * x_val
    x_ship += l_move
    x_waypoint += l_move
  else:
    assert 0, "Invalid cmd {}{}".format(x_cmd, x_val)

  return (x_ship, x_waypoint)

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()