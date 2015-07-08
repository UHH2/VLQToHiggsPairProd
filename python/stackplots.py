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


def plotter_factory(factor=1., **kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_sigxfactor(w, factor)
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)



