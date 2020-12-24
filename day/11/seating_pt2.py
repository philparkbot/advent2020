#!/usr/bin/env python3

import argparse
import copy

#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Seating (Advent 2020 day 11')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_directions = [ 'N', 'S', 'E', 'W', 'NE', 'SE', 'NW', 'SW' ]
  l_next_seating = open(g_args.m_file).readlines()
  l_next_seating = [ x.rstrip() for x in l_next_seating ]
  l_next_seating = [ list(x) for x in l_next_seating ] # convert from string to list of characters for mutable access
  l_max_row_id = len(l_next_seating) - 1
  l_max_col_id = len(l_next_seating[0]) - 1

  if g_args.m_debug:
    print("Max row:{}, max col:{}".format(l_max_row_id, l_max_col_id))

  l_current_seating = None
  l_iter = 0

  if g_args.m_debug:
    print("Initial state:")
    print_state(l_next_seating)

  while l_next_seating != l_current_seating:
    l_current_seating = copy.deepcopy(l_next_seating)

    for l_curr_row_id in range(l_max_row_id+1):
      for l_curr_col_id in range(l_max_col_id+1):
        l_curr_sq = l_current_seating[l_curr_row_id][l_curr_col_id]
        if l_curr_sq == '.': continue

        # now only process empty/occupied seats from here
        l_count = 0
        for l_dir in l_directions:
          l_count += count_occupied_seats(l_current_seating, l_curr_row_id, l_curr_col_id, l_dir)

          # optimization: break out early
          if l_curr_sq == 'L' and l_count > 0: break

        if l_curr_sq == 'L' and l_count == 0: l_next_seating[l_curr_row_id][l_curr_col_id] = '#'
        if l_curr_sq == '#' and l_count >= 5: l_next_seating[l_curr_row_id][l_curr_col_id] = 'L'
    
    print("Iteration {}: state change={}".format(l_iter, l_next_seating != l_current_seating), flush=True)
    if g_args.m_debug:
      print_state(l_next_seating)
    l_iter += 1
  
  # count all occupied seats
  l_count = 0
  for l_curr_row_id in range(l_max_row_id+1):
    for l_curr_col_id in range(l_max_col_id+1):
      l_sq = l_current_seating[l_curr_row_id][l_curr_col_id]
      if l_sq == '#': l_count += 1
  
  print("Count is {}".format(l_count))


#------------------------------------------------------------------------------
def print_state(x_seating):
#------------------------------------------------------------------------------
  for l_row in x_seating:
    for l_sq in l_row:
      print('{}'.format(l_sq), end='')
    print("")

#------------------------------------------------------------------------------
def count_occupied_seats(x_current_seating, x_x, x_y, x_direction):
#------------------------------------------------------------------------------
  l_count = 0
  l_done = False
  l_x_incr = 0
  l_y_incr = 0
  l_curr_x = x_x
  l_curr_y = x_y

  if 'N' in x_direction:
    l_x_incr = -1
  if 'S' in x_direction:
    l_x_incr = 1
  if 'E' in x_direction:
    l_y_incr = 1
  if 'W' in x_direction:
    l_y_incr = -1

  while not l_done:
    try:
      l_curr_x += l_x_incr
      l_curr_y += l_y_incr
      l_sq = x_current_seating[l_curr_x][l_curr_y]

      if l_curr_x < 0 or l_curr_y < 0:
        l_done = True
      elif l_sq == 'L':
        l_done = True
      elif l_sq == '#':
        l_count += 1
        l_done = True
    except IndexError:
      l_done = True

  if g_args.m_debug:
    print("sq[{}][{}] dir={} curr={} count={}".format(x_x, x_y, x_direction, x_current_seating[x_x][x_y], l_count))
  assert l_count <= 1, "Count > 1"
  return l_count



#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()