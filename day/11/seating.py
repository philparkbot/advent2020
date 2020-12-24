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
  l_next_seating = open(g_args.m_file).readlines()
  l_next_seating = [ x.rstrip() for x in l_next_seating ]
  l_next_seating = [ list(x) for x in l_next_seating ]
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
        l_neighbors = compute_neighbors(l_curr_row_id, l_curr_col_id, l_max_row_id, l_max_col_id)
        l_count = count_occupied_seats(l_current_seating, l_curr_row_id, l_curr_col_id, l_neighbors)

        if l_curr_sq == 'L' and l_count == 0: l_next_seating[l_curr_row_id][l_curr_col_id] = '#'
        if l_curr_sq == '#' and l_count >= 4: l_next_seating[l_curr_row_id][l_curr_col_id] = 'L'
    
    if g_args.m_debug:
      print("Iteration {}: state change={}".format(l_iter, l_next_seating != l_current_seating))
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
def count_occupied_seats(x_current_seating, x_x, x_y, x_neighbors):
#------------------------------------------------------------------------------
  l_count = 0

  for l_coordinates in x_neighbors:
    (l_x, l_y) = l_coordinates
    try:
      if x_current_seating[l_x][l_y] == '#': l_count += 1
    except IndexError:
      print("{}/{} is out of range".format(l_x, l_y))

  if g_args.m_debug:
    print("Occupied neighbors at coordinates {}/{} is {}".format(x_x, x_y, l_count)) 
  return l_count


'''
A square can have up to 8 neighbors, or as low as 3 if it's in a corner
'''
#------------------------------------------------------------------------------
def compute_neighbors(x_row, x_col, x_max_row, x_max_col):
#------------------------------------------------------------------------------
  l_neighbors = list()

  for l_try_row in (x_row - 1, x_row, x_row + 1):
    for l_try_col in (x_col - 1, x_col, x_col + 1):
      if l_try_row == x_row and l_try_col == x_col: continue
      if l_try_row < 0: continue
      if l_try_col < 0: continue
      if l_try_row > x_max_row: continue
      if l_try_col > x_max_col: continue
      l_coordinates = (l_try_row, l_try_col)
      l_neighbors.append(l_coordinates)
  
  return l_neighbors



#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()