#!/usr/bin/env python3

'''
Check various fields of a passport to determine if it's valid. Each entry can span more than one line,
but a blank line indicates the end of the entry.

Fields:
byr (birth year)
iyr (issue year)
eyr (expiration year)
hgt (height)
hcl (hair color)
ecl (eye color)
pid (passport ID)
cid (country ID)

cid is the only field that's considered optional. Only passports with all entries except cid are valid.
'''

g_file = 'input.txt'

g_fields = ['byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            'cid']

g_all_entries = list()
g_valid_entries = list()
g_debug = True

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  global g_all_entries
  global g_valid_entries
  l_entry = None
  l_entry_id = -1

  for l_line in open(g_file).readlines():
    l_line = l_line.rstrip()
    if l_entry == None:
      l_entry = dict()
      l_entry_id += 1
      l_entry['id'] = l_entry_id
    
    if ':' not in l_line:
      l_valid = process_entry(l_entry)
      g_all_entries.append(l_entry)
      if l_valid: g_valid_entries.append(l_entry)
      l_entry = None
      continue
    
    l_items = l_line.split(' ')
    for l_item in l_items:
      (l_key, l_val) = l_item.split(':')
      l_entry[l_key] = l_val
    
  if l_entry:
    l_valid = process_entry(l_entry)
    g_all_entries.append(l_entry)
    if l_valid: g_valid_entries.append(l_entry)

  l_valid_count = len(g_valid_entries)
  l_total_count = len(g_all_entries)
  print("There are {} valid entries out of {} total entries".format(l_valid_count, l_total_count))

#------------------------------------------------------------------------------
def process_entry(x_entry):
#------------------------------------------------------------------------------  
  l_valid = True

  l_msg = "Entry {}".format(x_entry['id'])
  for l_key, l_val in x_entry.items():
    l_msg += " {}:{}".format(l_key, l_val)

  l_missing = ''
  for l_field in g_fields:
    if l_field == 'cid': continue
    if l_field not in x_entry:
      l_missing += '{} '.format(l_field)
      l_valid = False
  
  l_msg = "valid:{} ".format(l_valid) + l_msg + " missing: " + l_missing
  if g_debug:
    print("{}".format(l_msg))
  
  return l_valid
#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()
main()