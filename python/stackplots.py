#!/usr/bin/env python

import common_vlq
import settings

import os
import time
import varial.generators as gen
import varial.rendering as rnd
import varial.tools

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

# def norm_siingletfactor(wrps, factor=1.):
#     for w in wrps:
#         if w.sample == 'SingleT_tChannel':
#             w.lumi /= factor
#             w = varial.op.norm_to_lumi(w)
#         yield w

def loader_hook_norm_smpl(wrps, smpl_fct=None):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    # wrps = norm_siingletfactor(wrps, singletfactor)
    wrps = common_vlq.merge_samples(wrps)
    wrps = common_vlq.merge_decay_channels(wrps,
        ('_thth', '_thtz', '_thbw'),
        '_thX'
    )
    wrps = common_vlq.merge_decay_channels(wrps,
        ('_noH_tztz', '_noH_tzbw', '_noH_bwbw'),
        '_other'
    )
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    wrps = norm_smpl(wrps, smpl_fct)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps

def loader_hook(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    # wrps = norm_sigxfactor(wrps)
    return wrps

# def loader_hook_sigxfactor(wrps, factor=1.):
#     wrps = loader_hook(wrps)
#     wrps = norm_sigxfactor(wrps, factor)
#     return wrps


def plotter_factory(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_norm_smpl(w, smpl_fct)
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)



