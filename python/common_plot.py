import os

import varial.analysis
import varial.generators as gen

import UHH2.VLQSemiLepPreSel.common as vlq_common

#====DEFINITIONS====

src_dir_rel = '../Hadd'

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
    'Run2015D',
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

def file_select(datasets_to_plot=common_datasets_to_plot, src=''):
    if src:
        src_dir = src
    else:
        src_dir = varial.analysis.cwd+src_dir_rel

    file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and '.sframe' not in f
            and any(g in f for g in datasets_to_plot)
        )]
    return file_list

    

#====GENERAL FUNCTIONS====

def merge_samples(wrps):
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_Pt80to120_MuEnr',
        '_Pt120to170_MuEnr',
        '_Pt170to300_MuEnr',
        '_Pt300to470_MuEnr',
        '_Pt470to600_MuEnr',
        '_Pt600to800_MuEnr',
        '_Pt800to1000_MuEnr',
        '_Pt1000toInf_MuEnr',
    ), print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, (
        'ToLL_HT100to200',
        'ToLL_HT200to400',
        'ToLL_HT400to600',
        'ToLL_HT600toInf',
    ), print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_tChannel',
        '_WAntitop',
        '_WTop',
        '_sChannel',
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
    ), print_warning=False)
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

# @history.track_history
def scale_signal(wrp, fct=1.):
    if fct >= 5:
        fct = int(fct)
        if fct % 5 > 2:
            fct += fct % 5
        else: fct -= fct % 5
    elif fct >= 1.:
        fct = int(fct)
    elif fct >= 0.2:
        fct = 1
    else:
        fct *= 5
    wrp.histo.Scale(fct)
    if fct > 1:
        wrp.legend +=' (x%.2g)' % fct
    elif fct < 1:
        wrp.legend +=' (x%.1g)' % fct

def norm_to_bkg(grps):
    for g in grps:
        bkg = g.wrps[0]
        if not (bkg.is_signal or bkg.is_data):
            max_bkg = bkg.histo.GetMaximum()
            max_sig = 0.
            for w in g.wrps:
                if w.is_signal:
                    if not max_sig:
                        max_sig = w.histo.GetMaximum()
                        fct_val = (max_bkg/max_sig)*0.2
                    scale_signal(w, fct_val)            
        yield g


def mod_legend(wrps):
    for w in wrps:
        if w.legend.startswith('MC_'):
            w.legend = w.legend[3:]
        yield w

#====LOADER HOOKS====

def loader_hook(wrps):
    wrps = vlq_common.add_wrp_info(wrps, sig_ind=signal_indicators)
    wrps = gen.sort(wrps)
    wrps = mod_legend(wrps)
    # wrps = merge_samples(wrps)
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




#====FOR STACKPLOTS====

def loader_hook_norm_smpl(wrps, smpl_fct=None):
    wrps = loader_hook(wrps)
    # wrps = gen.sort(wrps, key_list=['in_file_path', 'sample'])
    wrps = norm_smpl(wrps, smpl_fct)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps

def stack_setup_norm_sig(grps):
    grps = gen.mc_stack_n_data_sum(grps)
    grps = norm_to_bkg(grps)
    return grps

def plotter_factory_stack(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_norm_smpl(w, smpl_fct)
    kws['plot_setup'] = stack_setup_norm_sig
    kws['stack_setup'] = stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]

#====FOR NORMPLOTS====

def loader_hook_norm_to_int(wrps):
    wrps = loader_hook(wrps)
    # wrps = gen.sort(wrps, key_list=['in_file_path', 'sample'])
    # wrps = gen.switch(
    #     wrps,
    #     lambda w: w.in_file_path.split('/')[0] == 'GenHists',
    #     gen.gen_make_th2_projections
    # )
    # wrps = gen.gen_make_eff_graphs(wrps)
    wrps = gen.switch(
        wrps,
        lambda w: 'TH' in w.type,
        gen.gen_noex_norm_to_integral
    )
    return wrps


def plotter_factory_norm(**kws):
    kws['hook_loaded_histos'] = loader_hook_norm_to_int
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)



