#!/usr/bin/env python3

import re

'''
This is just a binary encoding problem. Seating is encoded like this:
'FBFBBFFRLR'

F/B: row
F = 0
B = 1

R/L: col
R = 1
L = 0

FBFBBFFRLR->
row: 0101100b = 44
col: 101b = 5

Seat ID = row * 8 + col = 357

'''

g_file = 'input.txt'
g_debug = True

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_highest = 0

  for l_line in open(g_file).readlines():
    l_line = l_line.rstrip()

    # split the encoding into row/col sections
    l_row = l_line[0:7]
    l_col = l_line[7:10]

    l_row = re.sub('F', '0', l_row)
    l_row = re.sub('B', '1', l_row)

    l_col = re.sub('L', '0', l_col)
    l_col = re.sub('R', '1', l_col)

    (l_row_id, l_col_id, l_seat_id) = decode(l_row, l_col)

    if g_debug:
      print("Seat encoding:{}, row:{}, col:{}, seat ID:{}".format(l_line, l_row_id, l_col_id, l_seat_id))

    l_highest = l_seat_id if l_seat_id > l_highest else l_highest

  print("Highest seat ID is {}".format(l_highest))

#------------------------------------------------------------------------------
def decode(x_row, x_col):
#------------------------------------------------------------------------------
  l_row_id = int(x_row, base=2)
  l_col_id = int(x_col, base=2)

  return (l_row_id, l_col_id, (l_row_id * 8 + l_col_id))

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()
main()
