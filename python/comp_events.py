#!/usr/bin/env python

import sys
import pprint

ref_file = sys.argv[1]
comp_file = sys.argv[2]

def mod_prec_mine(line):
	if not line:
		return ''
	pt, eta, phi, e = line.split(' ')[:4]
	return e, pt, eta, phi

def mod_prec_julie(line):
	if not line:
		return ''
	pt, eta, phi, e = line.split(' ')[:4]
	return e, pt, eta, phi

with open(ref_file, 'r') as r:
	ref_list = r.read()
	ref_list = ref_list.split('\n')
	ref_set = set(list(mod_prec_mine(l) for l in ref_list))


with open(comp_file, 'r') as c:
	comp_list = c.read()
	comp_list = comp_list.split('\n')
	comp_set = set(list(mod_prec_julie(l) for l in comp_list))

overlap_set = ref_set & comp_set
# pprint.pprint(ref_set)
print 'overlap between %s and %s: ' % (ref_file, comp_file), len(overlap_set)
print 'number of files in reference/comparison list and ratio: %s / %s / %s: ' % (len(ref_set), len(comp_set), float(len(overlap_set))/float(len(ref_set)))
if len(sys.argv) > 3:
	out_file = sys.argv[3]
	with open(out_file, 'w') as out:
		for line_ref in ref_list:
			if mod_prec_mine(line_ref) in overlap_set:
				# line_comp = ''
				for line_comp in comp_list:
					if mod_prec_julie(line_comp) == mod_prec_mine(line_ref):
						break
				out.write(line_ref + '\n')
				out.write(line_comp + '\n')
				out.write('-------\n')
