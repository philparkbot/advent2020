#!/usr/bin/env python3

'''
password file
<lo-hi policy> <letter>: <passwd>
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

The first field is a policy stating the minimum and maximum number of occurrences of <letter> in <passwd>.

The goal is to count the number of passwords from the input that adhere to the policy
'''

l_verbose = True
l_file = 'input.txt'
l_passwd_ok = 0

for l_entry in open(l_file).readlines():
  l_fields = l_entry.split(' ')
  l_policy = l_fields[0]
  (l_lo, l_hi) = l_policy.split('-')
  l_lo = int(l_lo)
  l_hi = int(l_hi)

  l_char = l_fields[1][0]
  l_passwd = l_fields[2].rstrip()

  l_count = l_passwd.count(l_char)
  l_ok = l_count >= l_lo and l_count <= l_hi
  if l_ok:
    l_passwd_ok += 1

  print("entry {}: '{}'. Count:{}".format('pass' if l_ok else 'fail', l_entry.rstrip(), l_passwd_ok))

print("{} entries adhere to policy".format(l_passwd_ok))

