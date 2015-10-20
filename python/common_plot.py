import os

import varial.analysis
import varial.generators as gen

import UHH2.VLQSemiLepPreSel.common as vlq_common

#====DEFINITIONS====

src_dir_rel = '../SFrame'

normfactors = {
    # 'TpTp' : 5.,
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

signal_indicators = ['TpTp']

common_datasets_to_plot = [
    'Run2015B',
    # 'TpTp_M-700',
    'TpTp_M-800',
    # 'TpTp_M-900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    'QCD',
    # 'TTbar',
    'TTbar',
    'WJets',
    'ZJets',
    'SingleT',
]

#====SELECT_FILES FUNCTIONS====

def file_selected_unsplit(datasets_to_plot=common_datasets_to_plot):
    src_dir = varial.analysis.cwd+src_dir_rel
    file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and '.sframe' not in f
            and any(g in f for g in datasets_to_plot)
        )]
    return file_list

def file_selected_split(datasets_to_plot=common_datasets_to_plot):
    src_dir = varial.analysis.cwd+src_dir_rel
    file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and '.sframe' not in f
            and any(g in f for g in datasets_to_plot)
            and not ('TpTp' in f and f.endswith('00.root'))
        )]
    return file_list

def file_stack_all_unsplit():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and '.sframe' not in f
        		)]
	return file_list

def file_stack_all_split():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and '.sframe' not in f
            and not ('TpTp' in f and f.endswith('00.root'))
		)]
	return file_list

def file_no_signals():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and '.sframe' not in f
            and 'TpTp' not in f
		)]
	return file_list

def file_split_signals():
	src_dir = varial.analysis.cwd+src_dir_rel
	file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
		(f.endswith('.root') and '.sframe' not in f
            and ('TpTp' in f and not f.endswith('00.root'))
		)]
	return file_list

def file_stack_less_signal_split():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and '.sframe' not in f
            and not ('TpTp' in f and f.endswith('00.root'))\
            and not any(g in f for g in ['TpTp_M-900', 'TpTp_M-1000', 'TpTp_M-1100', 'TpTp_M-1300'])
        )]
    return file_list

    

#====GENERAL FUNCTIONS====

def merge_samples(wrps):
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_Pt15to30',
        '_Pt30to50',
        '_Pt50to80',
        '_Pt80to120',
        '_Pt120to170',
        '_Pt170to300',
        '_Pt300to470',
        '_Pt470to600',
        '_Pt600to800',
        '_Pt800to1000',
        '_Pt1000to1400',
        '_Pt1400to1800',
        '_Pt1800to2400',
        '_Pt2400to3200',
        '_Pt3200toInf',
    ), print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, (
        'M10to50',
        'M50toInf',
    ), print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_tChannel',
        '_WAntitop',
        '_WTop',
    ))
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_Mtt0to700',
        '_Mtt700to1000',
        '_Mtt1000toInf',
    ))
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_LNu_HT100To200',
        '_LNu_HT200To400',
        '_LNu_HT400To600',
        '_LNu_HT600To800',
        '_LNu_HT800To1200',
        '_LNu_HT1200To2500',
        '_LNu_HT2500ToInf',        
    ))
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_Ele',
        '_Mu',
        '_Had'
    ), print_warning=False)
    return wrps

def norm_smpl(wrps, smpl_fct=None, norm_all=1.):
    for w in wrps:
        if smpl_fct:
            for fct_key, fct_val in smpl_fct.iteritems():
                if fct_key in w.sample:
                    # if w.analyzer = 'NoSelection' or 
                    w.lumi /= fct_val
                    w = varial.op.norm_to_lumi(w)
        w.lumi /= norm_all
        w = varial.op.norm_to_lumi(w)
        yield w

def loader_hook(wrps):
    wrps = vlq_common.add_wrp_info(wrps, sig_ind=signal_indicators)
    wrps = gen.sort(wrps)
    wrps = merge_samples(wrps)
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_wH_thth', '_wH_thtz', '_wH_thbw'),
        '_thX', print_warning=False
    )
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_thth', '_thtz', '_thbw'),
        '_thX', print_warning=False
    )
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_noH_tztz', '_noH_tzbw', '_noH_bwbw'),
        '_other', print_warning=False
    )
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    # wrps = norm_sigxfactor(wrps)
    return wrps
