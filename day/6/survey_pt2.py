#!/usr/bin/env python3


'''
Input is a group of one or more lines with letters.

Each letter = question to which the answer was 'yes'.
Each line represents survey answers by a person, contains one or more letter.
Adjacent lines are part of the same group.

For each group, count the number of questions to which all people answered 'yes'
'''

g_file = 'input.txt'

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_all_groups = list()
  l_curr_group = list()

  for l_line in open(g_file).readlines():
    l_line = l_line.rstrip()

    if len(l_line) == 0:
      # end of group, evaluate the current group's answers
      l_tmp = None
      for l_person in l_curr_group:
        if l_tmp == None:
          l_tmp = l_person
        else:
          l_tmp = l_tmp.intersection(l_person)

      l_all_groups.append(l_tmp)
      l_curr_group = list()
      continue

    l_person = set()

    for l_idx in range(len(l_line)):
      l_person.add(l_line[l_idx])
    
    l_curr_group.append(l_person)
  
  if len(l_curr_group) > 0:
    l_tmp = None
    for l_person in l_curr_group:
      if l_tmp == None:
        l_tmp = l_person
      else:
        l_tmp = l_tmp.intersection(l_person)

    l_all_groups.append(l_tmp)

  # now count
  l_sum = 0
  for l_idx, l_entry in enumerate(l_all_groups):
    l_sum += len(l_entry)
    print("Group {}: {} ({})".format(l_idx, len(l_entry), l_entry))

  print("Count is {}".format(l_sum))



#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()
main()