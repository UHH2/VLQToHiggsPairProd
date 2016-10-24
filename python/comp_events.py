#!/usr/bin/env python

import sys

ref_file = sys.argv[1]
comp_file = sys.argv[2]

with open(ref_file, 'r') as r:
	ref_list = r.read()
	ref_list = ref_list.split('\n')
	ref_set = set(list(tuple(l.split(' ')[:3]) for l in ref_list))


with open(comp_file, 'r') as c:
	comp_list = c.read()
	comp_list = comp_list.split('\n')
	comp_set = set(list(tuple(l.split(' ')[:3]) for l in comp_list))

overlap_set = ref_set & comp_set
print 'overlap between %s and %s: ' % (ref_file, comp_file), len(overlap_set)
if len(sys.argv) > 3:
	out_file = sys.argv[3]
	with open(out_file, 'w') as out:
		for line in ref_list:
			if tuple(line.split(' ')[:3]) in overlap_set:
				out.write(line + '\n')
