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

import re

g_file = 'input.txt'

g_fields = ['byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            'cid']

g_ecl = [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ]
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



'''
New rules for fields:
+ byr (Birth Year) - four digits; at least 1920 and at most 2002.
+ iyr (Issue Year) - four digits; at least 2010 and at most 2020.
+ eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
+ hgt (Height) - a number followed by either cm or in:
+  - If cm, the number must be at least 150 and at most 193.
+  - If in, the number must be at least 59 and at most 76.
+ hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
+ ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
+ pid (Passport ID) - a nine-digit number, including leading zeroes.
+ cid (Country ID) - ignored, missing or not.

'''
#------------------------------------------------------------------------------
def process_entry(x_entry):
#------------------------------------------------------------------------------  
  l_valid = True

  l_msg = "Entry {}".format(x_entry['id'])
  for l_key, l_val in x_entry.items():
    l_msg += " {}:{}".format(l_key, l_val)

  l_missing = ''
  l_reason = ''
  for l_field in g_fields:
    if l_field == 'cid': continue
    if l_field not in x_entry:
      l_missing += '{} '.format(l_field)
      l_valid = False
      continue
    
    l_val = x_entry[l_field]
    if l_field == 'byr':
      l_num = int(l_val)
      if not (l_num >= 1920 and l_num <= 2002 and len(l_val) == 4):
        l_valid = False
        l_reason += "{} ".format(l_field)

    if l_field == 'iyr':
      l_num = int(l_val)
      if not (l_num >= 2010 and l_num <= 2020 and len(l_val) == 4):
        l_valid = False
        l_reason += "{} ".format(l_field)
    
    if l_field == 'eyr':
      l_num = int(l_val)
      if not (l_num >= 2020 and l_num <= 2030 and len(l_val) == 4):
        l_valid = False
        l_reason += "{} ".format(l_field)
    
    if l_field == 'hgt':
      if 'cm' in l_val:
        l_idx = l_val.find('cm')
        l_height = int(l_val[0:l_idx])
        if not (l_height >= 150 and l_height <= 193):
          l_valid = False
          l_reason += "{} ".format(l_field)
      elif 'in' in l_val:
        l_idx = l_val.find('in')
        l_height = int(l_val[0:l_idx])
        if not (l_height >= 59 and l_height <= 76):
          l_valid = False
          l_reason += "{} ".format(l_field)
      else:
        l_valid = False
        l_reason += "{} ".format(l_field)
    
    if l_field == 'hcl':
      l_match = re.match('#([0-9a-f]){6}$', l_val)
      if not l_match:
        l_valid = False
        l_reason += "{} ".format(l_field)

    if l_field == 'ecl':
      if l_val not in g_ecl:
        l_valid = False
        l_reason += "{} ".format(l_field)

    if l_field == 'pid':
      l_match = re.fullmatch('(\d){9}', l_val)
      if not l_match:
        l_valid = False
        l_reason += "{} ".format(l_field)

  l_msg = "valid:{} ".format(l_valid) + l_msg + " missing: " + l_missing + "reason: " + l_reason
  if g_debug:
    print("{}".format(l_msg))
  
  return l_valid
#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()
main()