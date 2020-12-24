#!/usr/bin/env python3


'''
Input is a group of one or more lines with letters.

Each letter = question to which the answer was 'yes'.
Each line represents survey answers by a person, contains one or more letter.
Adjacent lines are part of the same group.

For each group, count the number of questions to which anyone answered 'yes'.
Find the sum of the counts.

'''

g_file = 'input.txt'

#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_group = set()
  l_all_groups = list()

  for l_line in open(g_file).readlines():
    l_line = l_line.rstrip()

    if len(l_line) == 0:
      # end of group
      l_all_groups.append(l_group)
      l_group = set()
      continue

    for l_idx in range(len(l_line)):
      l_group.add(l_line[l_idx])
  
  if l_group:
    l_all_groups.append(l_group)

  # now count
  l_sum = 0
  for l_idx, l_entry in enumerate(l_all_groups):
    l_sum += len(l_entry)
    #print("Group {}: {} ({})".format(l_idx, len(l_entry), l_entry))

  print("Count is {}".format(l_sum))



#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()


main()