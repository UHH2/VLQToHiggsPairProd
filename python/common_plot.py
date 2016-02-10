import os

import varial.analysis
import varial.generators as gen

import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.operations as op

#====DEFINITIONS====

src_dir_rel = '../Hadd'

basenames_final = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015D',
    'DATA.SingleEle_Run2015D',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TpTp_M-0700_thth', 'MC.TpTp_M-0700_thtz', 'MC.TpTp_M-0700_thbw', 'MC.TpTp_M-0700_noH_tztz', 'MC.TpTp_M-0700_noH_tzbw', 'MC.TpTp_M-0700_noH_bwbw',
    'MC.TpTp_M-0800_thth', 'MC.TpTp_M-0800_thtz', 'MC.TpTp_M-0800_thbw', 'MC.TpTp_M-0800_noH_tztz', 'MC.TpTp_M-0800_noH_tzbw', 'MC.TpTp_M-0800_noH_bwbw',
    'MC.TpTp_M-0900_thth', 'MC.TpTp_M-0900_thtz', 'MC.TpTp_M-0900_thbw', 'MC.TpTp_M-0900_noH_tztz', 'MC.TpTp_M-0900_noH_tzbw', 'MC.TpTp_M-0900_noH_bwbw',
    'MC.TpTp_M-1000_thth', 'MC.TpTp_M-1000_thtz', 'MC.TpTp_M-1000_thbw', 'MC.TpTp_M-1000_noH_tztz', 'MC.TpTp_M-1000_noH_tzbw', 'MC.TpTp_M-1000_noH_bwbw',
    'MC.TpTp_M-1100_thth', 'MC.TpTp_M-1100_thtz', 'MC.TpTp_M-1100_thbw', 'MC.TpTp_M-1100_noH_tztz', 'MC.TpTp_M-1100_noH_tzbw', 'MC.TpTp_M-1100_noH_bwbw',
    'MC.TpTp_M-1200_thth', 'MC.TpTp_M-1200_thtz', 'MC.TpTp_M-1200_thbw', 'MC.TpTp_M-1200_noH_tztz', 'MC.TpTp_M-1200_noH_tzbw', 'MC.TpTp_M-1200_noH_bwbw',
    'MC.TpTp_M-1300_thth', 'MC.TpTp_M-1300_thtz', 'MC.TpTp_M-1300_thbw', 'MC.TpTp_M-1300_noH_tztz', 'MC.TpTp_M-1300_noH_tzbw', 'MC.TpTp_M-1300_noH_bwbw',
    'MC.TpTp_M-1400_thth', 'MC.TpTp_M-1400_thtz', 'MC.TpTp_M-1400_thbw', 'MC.TpTp_M-1400_noH_tztz', 'MC.TpTp_M-1400_noH_tzbw', 'MC.TpTp_M-1400_noH_bwbw',
    'MC.TpTp_M-1500_thth', 'MC.TpTp_M-1500_thtz', 'MC.TpTp_M-1500_thbw', 'MC.TpTp_M-1500_noH_tztz', 'MC.TpTp_M-1500_noH_tzbw', 'MC.TpTp_M-1500_noH_bwbw',
    'MC.TpTp_M-1600_thth', 'MC.TpTp_M-1600_thtz', 'MC.TpTp_M-1600_thbw', 'MC.TpTp_M-1600_noH_tztz', 'MC.TpTp_M-1600_noH_tzbw', 'MC.TpTp_M-1600_noH_bwbw',
    'MC.TpTp_M-1700_thth', 'MC.TpTp_M-1700_thtz', 'MC.TpTp_M-1700_thbw', 'MC.TpTp_M-1700_noH_tztz', 'MC.TpTp_M-1700_noH_tzbw', 'MC.TpTp_M-1700_noH_bwbw',
    'MC.TpTp_M-1800_thth', 'MC.TpTp_M-1800_thtz', 'MC.TpTp_M-1800_thbw', 'MC.TpTp_M-1800_noH_tztz', 'MC.TpTp_M-1800_noH_tzbw', 'MC.TpTp_M-1800_noH_bwbw',
    ])

basenames_pre = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015D',
    'DATA.SingleEle_Run2015D',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TpTp_M-0700',
    'MC.TpTp_M-0800',
    'MC.TpTp_M-0900',
    'MC.TpTp_M-1000',
    'MC.TpTp_M-1100',
    'MC.TpTp_M-1200',
    'MC.TpTp_M-1300',
    'MC.TpTp_M-1400',
    'MC.TpTp_M-1500',
    'MC.TpTp_M-1600',
    'MC.TpTp_M-1700',
    'MC.TpTp_M-1800',
    ])

normfactors = {
    # 'TpTp' : 5.,
    '_thX' : 1./0.56,
    '_other' : 1./0.44,
    'TpTp_M-0700' : 1./0.455,
    'TpTp_M-0800' : 1./0.196,
    'TpTp_M-0900' : 1./0.0903,
    'TpTp_M-1000' : 1./0.0440,
    'TpTp_M-1100' : 1./0.0224,
    'TpTp_M-1200' : 1./0.0118,
    'TpTp_M-1300' : 1./0.00639,
    'TpTp_M-1400' : 1./0.00354,
    'TpTp_M-1500' : 1./0.00200,
    'TpTp_M-1600' : 1./0.001148,
    'TpTp_M-1700' : 1./0.000666,
    'TpTp_M-1800' : 1./0.000391,
}

signal_indicators = ['TpTp_']

common_datasets_to_plot = [
    'Run2015D',
    'TpTp_M-0700',
    # 'TpTp_M-0800',
    # 'TpTp_M-0900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    'QCD',
    # 'TTbar',
    'TTbar',
    'WJets',
    'ZJets',
    'SingleTop',
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

def merge_finalstates_channels(wrps, finalstates=(), suffix='', print_warning=True):
    """histos must be sorted!!"""

    @varial.history.track_history
    def merge_decay_channel(w):
        return w

    def do_merging(buf):
        res = varial.operations.merge(buf)
        res.sample = res.sample+suffix
        res.legend = res.legend+suffix
        # res.in_file_path = buf[0].in_file_path[1:]
        del buf[:]
        return merge_decay_channel(res)

    buf = []
    for w in wrps:
        if any(w.finalstate == p for p in finalstates):
            buf.append(w)
            if len(buf) == len(finalstates):
                yield do_merging(buf)
        else:
            if buf:
                if print_warning:
                    print 'WARNING In merge_decay_channels: buffer not empty.\n' \
                          'finalstates:\n' + str(finalstates) + '\n' \
                          'Flushing remaining items:\n' + '\n'.join(
                        '%s, %s' % (w.sample, w.in_file_path) for w in buf
                    )
                yield do_merging(buf)
            yield w
    if buf:
        yield do_merging(buf)


def norm_smpl(wrps, smpl_fct=None, norm_all=1.):
    for w in wrps:
        if smpl_fct:
            for fct_key, fct_val in smpl_fct.iteritems():
                if fct_key in w.sample:
                    # if w.analyzer = 'NoSelection' or
                    if hasattr(w, 'scl_fct'):
                        w.scl_fct *= fct_val
                    else:
                        op.add_wrp_info(w, scl_fct=lambda _: fct_val)
                    w.histo.Scale(fct_val)
        if hasattr(w, 'scl_fct'):
            w.scl_fct *= norm_all
        else:
            op.add_wrp_info(w, scl_fct=lambda _: norm_all)
        w.histo.Scale(norm_all)
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
    if hasattr(wrp, 'scl_fct'):
        wrp.scl_fct *= fct
    else:
        op.add_wrp_info(wrp, scl_fct=lambda _: fct)
    wrp.histo.Scale(fct)
    if fct > 1:
        wrp.legend +=' (%.2g pb)' % fct
    elif fct < 1:
        wrp.legend +=' (%.1g pb)' % fct

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
        if w.is_data:
            w.legend = 'data'
        if w.legend.startswith('TpTp'):
            w.legend = 'TT M'+w.legend[7:]
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5]
        yield w

#====LOADER HOOKS====

def loader_hook(wrps):
    wrps = vlq_common.add_wrp_info(wrps, sig_ind=signal_indicators, use_hadd_sample=False)
    wrps = list(wrps)
    # wrps = gen.sort(wrps)
    wrps = mod_legend(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    # wrps = norm_sigxfactor(wrps)
    return wrps




#====FOR STACKPLOTS====

def loader_hook_norm_smpl(wrps, smpl_fct=None, rebin_max_bins=60):
    if rebin_max_bins:
        wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, rebin_max_bins)
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



