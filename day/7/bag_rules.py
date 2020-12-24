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

Example: You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
In the above rules, the following options would be available to you:
  - A bright white bag, which can hold your shiny gold bag directly.
  - A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
  - A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
  - A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag?

I'm probably going to create a reverse hash where the key is inner bag and the value is a list of corresponding outer bags.
'''

g_file = 'input.txt'


#------------------------------------------------------------------------------
def run():
#------------------------------------------------------------------------------
  l_rules = dict()
  for l_line in open(g_file).readlines():
    (l_outer, l_inner_list) = parse_rule(l_line)

    if l_inner_list == None:
      continue

    for l_tuple in l_inner_list:
      (l_quantity, l_desc) = l_tuple
      if l_desc not in l_rules: l_rules[l_desc] = list()
      l_rules[l_desc].append(l_outer)

  # now trace 
  l_bag_track = dict()

  traverse_rules('shiny gold', l_rules, l_bag_track)

  print("{} can hold shiny gold bags".format(len(l_bag_track.keys())))

#------------------------------------------------------------------------------
def traverse_rules(x_desc, x_rules, x_bag_track):
#------------------------------------------------------------------------------
  if x_desc not in x_rules: return

  for l_bag in x_rules[x_desc]:
    x_bag_track[l_bag] = True
    traverse_rules(l_bag, x_rules, x_bag_track)


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