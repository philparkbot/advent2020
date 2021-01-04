#!/usr/bin/env python3

import argparse
import re
import copy

'''
Input has three sections:
1. Fields containing ranges of valid values.
2. Your ticket with a list of comma-separated numbers indicating field values.
3. Neighboring ticket fields, one per line, of a list of comma-separated numbers indicating field values.

Part 2:

1. Parse ticket fields. Discard tickets with invalid values.
2. Using all valid tickets including your own, find out the order of fields for the tickets. All tickets
   have the same fields in the same order.
3. Goal: multiply the 6 departure fields on your ticket.

Steps:
1. Class for each number in the ticket matrix. Each row of comma separated numbers is a ticket. The first row is
   your ticket. The class contains value, row, col, candidate fields, and actual field.
2. Similar to sudoku. If the number of candidates is 1, then that is the field. Once that field is set, then no
   other number in the ticket can be that field, so eliminate it from other cells in the row.
3. All cells in the same column represent the same field. So if a cell is missing a field as a potential candidate,
   then *no other cell* in the same column could be that field.

'''

g_args = None

#------------------------------------------------------------------------------
class c_point():
#------------------------------------------------------------------------------
  # class variables go here

  #------------------------------------------------------------------------------
  def __init__(self, x_value, x_row_id, x_col_id):
  #------------------------------------------------------------------------------
    # instance variables go here
    self.m_value = x_value
    self.m_candidate_fields = set()
    self.m_row_id = x_row_id
    self.m_col_id = x_col_id
    self.m_field = None

  #------------------------------------------------------------------------------
  def string(self):
  #------------------------------------------------------------------------------
    if self.m_field == None:
      return "[{}][{}]: value:{}, {} candidates:{}".format(self.m_row_id, self.m_col_id, self.m_value, len(self.m_candidate_fields), self.m_candidate_fields)
    else:
      return "[{}][{}]: value:{}, field:{}".format(self.m_row_id, self.m_col_id, self.m_value, self.m_field)

  #------------------------------------------------------------------------------
  def id(self):
  #------------------------------------------------------------------------------
    return "[{}][{}]: value:{}".format(self.m_row_id, self.m_col_id, self.m_value)




#------------------------------------------------------------------------------
def options():
#------------------------------------------------------------------------------
  global g_args

  l_parser = argparse.ArgumentParser(description='Ticket validation (Advent 2020 day 16)')
  
  l_parser.add_argument('--file', dest='m_file', default='input.txt', help="Input file")
  l_parser.add_argument('--debug', dest='m_debug', default=False, action='store_true', help='Debug verbosity')
  g_args = l_parser.parse_args()

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_input = open(g_args.m_file).readlines()
  l_input = [ x.rstrip() for x in l_input ]

  l_ticket_fields = dict()

  l_num_cols = None
  l_curr_row = 0

  l_tickets = list()

  for l_line in l_input:
    # populate ticket fileds
    if ':' in l_line and ' or ' in l_line:
      l_field_name = l_line.split(':')[0]
      l_match = re.search(": (\d+)-(\d+) or (\d+)-(\d+)", l_line)

      assert l_match, "Sanity. Invalid line: {}".format(l_line)

      (l_lo0, l_hi0, l_lo1, l_hi1) = l_match.group(1,2,3,4)

      l_ticket_fields[l_field_name] = dict()
      l_ticket_fields[l_field_name]['range0'] = dict()
      l_ticket_fields[l_field_name]['range1'] = dict()

      l_ticket_fields[l_field_name]['range0']['lo'] = int(l_lo0)
      l_ticket_fields[l_field_name]['range0']['hi'] = int(l_hi0)
      l_ticket_fields[l_field_name]['range1']['lo'] = int(l_lo1)
      l_ticket_fields[l_field_name]['range1']['hi'] = int(l_hi1)
      continue

    if ',' not in l_line: continue

    if g_args.m_debug:
      print("Processing row {}: {}".format(l_curr_row, l_line))

    # now parse nearby tickets
    l_values = l_line.split(',')
    l_values = [ c_point(int(x), l_curr_row, col) for col, x in enumerate(l_values) ]

    l_tickets.append(l_values)

    if l_num_cols == None:
      l_num_cols = len(l_values)

    l_failing_val = None
    for l_point in l_values:
      l_valid = is_valid(l_ticket_fields, l_point.m_value)
      if not l_valid:
        l_failing_val = l_point.m_value
        if g_args.m_debug:
          print("row {}, value {} failed".format(l_curr_row, l_point.m_value))
        break

    if l_failing_val != None:
      if g_args.m_debug:
        print("row {} '{}', fail val:{}. Discarding ticket".format(l_curr_row, l_line, l_failing_val))
      l_tickets.pop()
      continue

    # at this piont we know the ticket only has valid values
    for l_point in l_values:
      l_fields = eligible_fields(l_ticket_fields, l_point.m_value)
      l_point.m_candidate_fields = set(l_fields)

    l_curr_row += 1

  '''
  Find any missing fields from eligible candidates and eliminate them from all points in the
  same column. Iterate until we don't have any more changes.
  '''
  l_change = True
  l_iter = 0

  while l_change:
    l_iter += 1
    l_change = False

    if g_args.m_debug:
      print("iter {}".format(l_iter), flush=True)
    for l_curr_ticket in l_tickets:
      for l_point in l_curr_ticket:
        if len(l_point.m_candidate_fields) < len(l_ticket_fields):
          l_missing = list(set(l_ticket_fields.keys()) - l_point.m_candidate_fields)

          if g_args.m_debug:
            print("Iter {}: removing '{}' from col {}".format(l_iter, l_missing, l_point.m_col_id))

          # now eliminate these fields from all other cells in the same column
          for l_field in l_missing:
            l_change |= eliminate_col(l_tickets, l_field, l_point.m_col_id)

  if g_args.m_debug:
    print("{} iterations of col eliminations".format(l_iter))

  '''
  See if we have any points left with a single possible candidate.
  Set the field for that point and all points in the same column, eliminate it from the candidate list on
  all other points in the same row.
  '''

  l_change = True
  l_iter = 0

  while l_change:
    l_iter += 1
    l_change = False

    for l_curr_ticket in l_tickets:
      for l_point in l_curr_ticket:
        if len(l_point.m_candidate_fields) == 1:
          l_field = l_point.m_candidate_fields.pop()
          l_point.m_field = l_field
          l_change |= eliminiate_row(l_curr_ticket, l_field)

  if g_args.m_debug:
    print("{} iterations of row eliminations".format(l_iter))

  if g_args.m_debug:
    for l_curr_ticket in l_tickets:
      for l_point in l_curr_ticket:
        print("{}".format(l_point.string()))
  
  l_answer = 1
  for l_point in l_tickets[0]:
    if 'departure' in l_point.m_field:
      l_answer *= l_point.m_value

  print("Answer is {}".format(l_answer))
  

  '''
  # find unique candidates in a row (ticket). A unique value belongs to that field.
  for l_curr_ticket in l_tickets:
    for l_idx, l_point in enumerate(l_curr_ticket):
      l_uniques = find_unique(l_idx, l_curr_ticket)
      if g_args.m_debug:
        print("[{}][{}]: uniques:{}".format(l_point.m_row_id, l_point.m_col_id, l_uniques))
  '''

   
#------------------------------------------------------------------------------
def eliminiate_row(x_ticket, x_field):
#------------------------------------------------------------------------------
  l_change = False

  for l_point in x_ticket:
    if x_field in l_point.m_candidate_fields:
      l_point.m_candidate_fields.remove(x_field)
      l_change = True
  
  return l_change

#------------------------------------------------------------------------------
def eliminate_col(x_tickets, x_field, x_col):
#------------------------------------------------------------------------------
  l_change = False

  for l_ticket in x_tickets:
    l_point = l_ticket[x_col]

    assert l_point.m_col_id == x_col, "sanity: column mismatch for cell [{}][{}] value {}".format(l_point.m_row_id, l_point.m_col_id, l_point.m_value)

    if x_field in l_point.m_candidate_fields:
      l_point.m_candidate_fields.remove(x_field)
      l_change = True
    
    if x_field in l_point.m_candidate_fields:
      assert 0, "sanity"
  
  return l_change

#------------------------------------------------------------------------------
def find_unique(x_idx, x_ticket):
#------------------------------------------------------------------------------
  l_my_candidates = copy.deepcopy(x_ticket[x_idx].m_candidate_fields)

  for l_idx, l_point in enumerate(x_ticket):
    if x_idx == l_idx: continue

    l_my_candidates = l_my_candidates - l_point.m_candidate_fields
  
  return l_my_candidates


'''
Return true if the value is valid for any field in the ticket
'''
#------------------------------------------------------------------------------
def is_valid(x_fields, x_num):
#------------------------------------------------------------------------------
  l_valid = False

  for l_field in x_fields:
    l_lo0 = x_fields[l_field]['range0']['lo']
    l_hi0 = x_fields[l_field]['range0']['hi']
    l_lo1 = x_fields[l_field]['range1']['lo']
    l_hi1 = x_fields[l_field]['range1']['hi']

    if (x_num >= l_lo0 and x_num <= l_hi0) or (x_num >= l_lo1 and x_num <= l_hi1):
      l_valid = True
      break
  
  return l_valid

'''
Return a list of fields that the value is valid for.
'''
#------------------------------------------------------------------------------
def eligible_fields(x_fields, x_num):
#------------------------------------------------------------------------------
  l_valid = False
  l_valid_fields = list()

  for l_field in x_fields:
    l_lo0 = x_fields[l_field]['range0']['lo']
    l_hi0 = x_fields[l_field]['range0']['hi']
    l_lo1 = x_fields[l_field]['range1']['lo']
    l_hi1 = x_fields[l_field]['range1']['hi']

    if (x_num >= l_lo0 and x_num <= l_hi0) or (x_num >= l_lo1 and x_num <= l_hi1):
      l_valid = True
      l_valid_fields.append(l_field)
  
  assert l_valid, "Invalid value {}. This shouldn't happen"
  return l_valid_fields

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()
