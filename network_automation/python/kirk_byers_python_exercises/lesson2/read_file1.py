#!/usr/bin/env python3


f = open('show_version.txt')

#print(f)

output = f.read()
print(repr(output))

f.close()
