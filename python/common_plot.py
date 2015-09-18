import os

import varial.analysis

src_dir_rel = '../SFrame'

normfactors = {
    'TpTp' : 5.,
    '_thX' : 1./0.56,
    '_other' : 1./0.44,
    'TpTp_M-700' : 1./0.455,
    'TpTp_M-800' : 1./0.196,
    'TpTp_M-900' : 1./0.0903,
    'TpTp_M-1000' : 1./0.0440,
    'TpTp_M-1100' : 1./0.0224,
    'TpTp_M-1200' : 1./0.0118,
    'TpTp_M-1300' : 1./0.00639,
    'TpTp_M-1400' : 1./0.00354,
    'TpTp_M-1500' : 1./0.00200,
    'TpTp_M-1600' : 1./0.001,
    'TpTp_M-1700' : 1./0.0005,
    'TpTp_M-1800' : 1./0.00025,
}

def file_stack_all_unsplit():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_stack_all_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root')
		)]
	return file_stack_all_list

def file_stack_all_split():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_stack_all_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and not ('TpTp' in f and f.endswith('00.root'))
		)]
	return file_stack_all_list

def file_no_signals():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_no_signals_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and 'TpTp' not in f
		)]
	return file_no_signals_list

def file_split_signals():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_no_signals_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and ('TpTp' in f and not f.endswith('00.root'))
		)]
	return file_no_signals_list