#!/usr/bin/env python3

import re

'''
Example rules:
* light red bags contain 1 bright white bag, 2 muted yellow bags.
* dark orange bags contain 3 bright white bags, 4 muted yellow bags.
* bright white bags contain 1 shiny gold bag.
* muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
* shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
* dark olive bags contain 3 faded blue bags, 4 dotted black bags.
* vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
* faded blue bags contain no other bags.
* dotted black bags contain no other bags.

Consider again your shiny gold bag and the rules from the above example:
* faded blue bags contain 0 other bags.
* dotted black bags contain 0 other bags.
* vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
* dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

'''

g_file = 'input.txt'


#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  '''
  l_rules['shiny gold'] = [ (1, 'dark olive'), (2, 'vibrant plum') ]
  '''
  l_rules = dict()
  for l_line in open(g_file).readlines():
    (l_outer, l_inner_list) = parse_rule(l_line)

    if l_inner_list == None:
      continue

    l_rules[l_outer] = l_inner_list

  l_count = count_bags('shiny gold', l_rules)

  print("1 shiny gold bag holds {} bags".format(l_count))

'''
count the number of bags contained by this bag type
'''
#------------------------------------------------------------------------------
def count_bags(x_desc, x_rules):
#------------------------------------------------------------------------------
  if x_desc not in x_rules: return 0

  l_total = 0
  for l_tuple in x_rules[x_desc]:
    (l_quantity, l_desc) = l_tuple
    l_total += l_quantity + l_quantity * count_bags(l_desc, x_rules)
  
  return l_total


'''
Parse a rule, returning:
(<outer bag description>, list())

If list is None, then the outer bag can't hold any bags.
Otherwise, the list contains tuples containing quantity and color of inner bags
'''
#------------------------------------------------------------------------------
def parse_rule(x_rule):
#------------------------------------------------------------------------------
  l_match = re.search("(.*) bags contain (.*)", x_rule)
  l_inner_list = None

  if not l_match:
    print("Error. No match for line {}".format(x_rule))
    exit(1)
  
  (l_outer, l_inner) = l_match.group(1, 2)

  if 'no other bags' in l_inner:
    pass
  else:
    l_inner_list = list()
    for l_sub in l_inner.split(','):
      l_curr_match = re.search("(\d+) (\w+\s\w+) bag", l_sub)
      if not l_curr_match:
        print("Error. No match on rule {} sub rule {}".format(x_rule, l_sub))
        exit(1)
      (l_quantity, l_style) = l_curr_match.group(1, 2)
      l_quantity = int(l_quantity)
      l_inner_list.append((l_quantity, l_style))

  return (l_outer, l_inner_list)

#------------------------------------------------------------------------------
def main():
#------------------------------------------------------------------------------
  run()
main()