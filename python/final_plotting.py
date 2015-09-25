#!/usr/bin/env python

import os
import time

import varial.generators as gen
import varial.rendering as rnd
import varial.tools

import UHH2.VLQSemiLepPreSel.common as vlq_common

import common_plot
# import tptp_settings

#====FOR STACKPLOTS====


def loader_hook_norm_smpl(wrps, smpl_fct=None):
    wrps = common_plot.loader_hook(wrps)
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_thth', '_thtz', '_thbw'),
        '_thX'
    )
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_noH_tztz', '_noH_tzbw', '_noH_bwbw'),
        '_other'
    )
    wrps = common_plot.norm_smpl(wrps, smpl_fct)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps

def plotter_factory_stack(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_norm_smpl(w, smpl_fct)
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)

#====FOR NORMPLOTS====

def loader_hook_norm_to_int(wrps):
    wrps = common_plot.loader_hook(wrps)
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_thth', '_thtz', '_thbw'),
        '_thX'
    )
    wrps = vlq_common.merge_decay_channels(wrps,
        ('_noH_tztz', '_noH_tzbw', '_noH_bwbw'),
        '_other'
    )
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



