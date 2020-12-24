#!/usr/bin/env python3

'''
password file
<pos1-pos2 policy> <letter>: <passwd>
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

pos1 and pos2 are the positions (indexed at 1) in the passwd that contain <letter>. Exactly one must match for the passwd to pass.
The first entry passes.
The second entry fails.
The third entry fails.

The goal is to count the number of passwords from the input that adhere to the policy
'''

l_verbose = True
l_file = 'input.txt'
l_passwd_ok = 0

for l_entry in open(l_file).readlines():
  l_fields = l_entry.split(' ')
  l_policy = l_fields[0]
  (l_pos1, l_pos2) = l_policy.split('-')
  l_pos1 = int(l_pos1)
  l_pos2 = int(l_pos2)

  l_char = l_fields[1][0]
  l_passwd = l_fields[2].rstrip()

  l_pass1 = l_passwd[l_pos1-1:l_pos1] == l_char
  l_pass2 = l_passwd[l_pos2-1:l_pos2] == l_char

  l_ok = bool(l_pass1) ^ bool(l_pass2)

  if l_ok:
    l_passwd_ok += 1

  print("entry {}: '{}'. Count:{}".format('pass' if l_ok else 'fail', l_entry.rstrip(), l_passwd_ok))

print("{} entries adhere to policy".format(l_passwd_ok))

