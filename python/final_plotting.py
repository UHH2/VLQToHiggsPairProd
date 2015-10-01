#!/usr/bin/env python

import os
import time

import varial.generators as gen
import varial.rendering as rnd
import varial.tools

import UHH2.VLQSemiLepPreSel.common as vlq_common

import common_plot
# import tptp_settings

def norm_to_bkg(grps):
    for g in grps:
        bkg = g.wrps[0]
        if not (bkg.is_signal or bkg.is_data):
            max_bkg = bkg.histo.GetMaximum()
            for w in g.wrps:
                if w.is_signal:
                    max_sig = w.histo.GetMaximum()
                    fct_val = (max_bkg/max_sig)*0.2
                    w.histo.Scale(fct_val)
                    w.legend +=' x%.1f' % fct_val
        yield g


#====FOR STACKPLOTS====

def loader_hook_norm_smpl(wrps, smpl_fct=None):
    wrps = common_plot.loader_hook(wrps)
    # wrps = gen.sort(wrps, key_list=['in_file_path', 'sample'])
    wrps = common_plot.norm_smpl(wrps, smpl_fct)
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
    return varial.tools.Plotter(**kws)

#====FOR NORMPLOTS====

def loader_hook_norm_to_int(wrps):
    wrps = common_plot.loader_hook(wrps)
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



