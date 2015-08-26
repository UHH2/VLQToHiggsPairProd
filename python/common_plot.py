import os

import varial.analysis

src_dir_rel = '../SFrame'

def file_stack_all_unsplit():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_stack_all_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root')
		)]
	return file_stack_all_list

def file_no_signals():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_no_signals_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and 'TpTp' not in f
		)]
	return file_no_signals_list