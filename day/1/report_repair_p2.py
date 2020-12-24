#!/usr/bin/env python3


'''
Given a list of numbers, find the three numbers (a, b, and c) that sum up to 2020. The answer is a * b * c.
'''

l_file = 'input.txt'

l_list = open(l_file).readlines()

l_first = 0

l_size = len(l_list)

for l_first in range(l_size):
  for l_second in range(l_first + 1, l_size):
    for l_third in range(l_second + 1, l_size):
      l_a = int(l_list[l_first])
      l_b = int(l_list[l_second])
      l_c = int(l_list[l_third])

      l_sum = l_a + l_b + l_c
      if l_sum == 2020:
        print("Found: {}, {}, and {}. Product:{}".format(l_a, l_b, l_c, l_a * l_b * l_c))