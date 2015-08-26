#!/usr/bin/env python

import common_vlq
import settings

import os
import time
import varial.generators as gen
import varial.rendering as rnd
import varial.tools

def norm_sigxfactor(wrps, factor=1.):
    for w in wrps:
        if w.is_signal:
            w.lumi /= factor
            w = varial.op.norm_to_lumi(w)
        yield w

def norm_siingletfactor(wrps, factor=1.):
    for w in wrps:
        if w.sample == 'SingleT_tChannel':
            w.lumi /= factor
            w = varial.op.norm_to_lumi(w)
        yield w

def loader_hook_norm_sig(wrps, sigxfactor=1.):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    # wrps = norm_siingletfactor(wrps, singletfactor)
    wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    wrps = norm_sigxfactor(wrps, sigxfactor)
    return wrps

def loader_hook(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    # wrps = norm_sigxfactor(wrps)
    return wrps

def loader_hook_sigxfactor(wrps, factor=1.):
    wrps = loader_hook(wrps)
    wrps = norm_sigxfactor(wrps, factor)
    return wrps


def plotter_factory(sigxfactor=1., **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_norm_sig(w, sigxfactor)
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)



