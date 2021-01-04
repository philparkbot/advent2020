#!/usr/bin/env python3

import argparse
import re

'''
Input has three sections:
1. Fields containing ranges of valid values.
2. Your ticket with a list of comma-separated numbers indicating field values.
3. Neighboring ticket fields, one per line, of a list of comma-separated numbers indicating field values.

Part 1 is to scan neighboring ticket fields, see if it contains any numbers that are invalid for all fields
specified for the first section, and log the error rate (sum of all invalid values).

1. Parse ticket fields. Store them in a dict.
2. For each ticket, iterate through the number list and compare them to ticket range. Any that fail in all fields is an invalid ticket.

Error rate is computed by summing all invalid values.
'''

g_args = None

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
  l_found = False

  l_sum = 0

  for l_idx, l_line in enumerate(l_input):
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
    elif not l_found:
      l_found = True if 'nearby tickets:' in l_line else l_found
      if g_args.m_debug:
        print("Line:{}, found={}".format(l_line, l_found))
      continue
    
    if not l_found: continue

    # now parse nearby tickets
    l_values = l_line.split(',')
    l_values = [ int(x) for x in l_values ]

    l_failing_val = None
    for l_num in l_values:
      l_valid = is_valid(l_ticket_fields, l_num)
      if not l_valid:
        l_failing_val = l_num
        l_sum += l_num
        if g_args.m_debug:
          print("line {}, value {} failed, adding to sum".format(l_idx, l_num))
    
    if g_args.m_debug:
      print("line {} '{}', fail val:{}".format(l_idx, l_line, l_failing_val))
    
  print("Ticket error rate is {}".format(l_sum))
    
'''
return True if the value is valid for any field in the ticket
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

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  options()
  run()
main()
