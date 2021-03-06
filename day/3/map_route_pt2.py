#!/usr/bin/env python3

import argparse

'''
Input file represents a map. '#' represents trees, '.' represents free space. Traverse the map down and to the right
in steps of the x/y increments. If you go past the last character in the X direction, you wrap back around. You are
done when you reach the last row. The goal is to count the number of trees in your route.
'''

l_file = 'input.txt'

l_row = 0
l_col = 0

l_parser = argparse.ArgumentParser(description='Python Advent 2020, day 3 part 2')
l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug level verbosity')
l_parser.add_argument('--x', dest='m_x', default=1, type=int, help='X increment')
l_parser.add_argument('--y', dest='m_y', default=1, type=int, help='Y increment')

l_args = l_parser.parse_args()

l_x_increment = l_args.m_x
l_y_increment = l_args.m_y

l_x_size = None
l_debug = l_args.m_debug

'''
[ ] Calculate next row/col values. Handle wraparound for column.
[ ] Iterate through each row until you reach next_row.
[ ] Move until you reach the next column.
[ ] When you have arrived, check if you're on a tree or free land, and increment if tree.
[ ] Repeat the first step.
'''
l_curr_col = 0
l_next_row = l_y_increment
l_next_col = l_x_increment
l_tree_count = 0


for l_curr_row, l_line in enumerate(open(l_file).readlines()):
  l_line = l_line.rstrip()

  if l_x_size == None:
    l_x_size = len(l_line)

    if l_debug:
      print("length is {}".format(l_x_size))

  if l_curr_row < l_next_row: continue

  l_curr_col = l_next_col

  # At this point, we're at the correct coordinates. Read

  l_spot = l_line[l_curr_col]
  l_is_tree = l_spot == '#'

  if l_is_tree:
    l_tree_count += 1

  if l_debug:
    l_list = list(l_line)
    l_list[l_curr_col] = 'X' if l_is_tree else 'O'
    l_line = ''.join(l_list)
    l_line = l_line.rstrip()

    print("{}: [{}][{}]".format(l_line, l_curr_row, l_curr_col))

  l_next_row += l_y_increment
  l_next_col = (l_next_col + l_x_increment) % l_x_size


print("There were {} trees".format(l_tree_count))

