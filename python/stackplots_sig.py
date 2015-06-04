#!/usr/bin/env python

import common_vlq
import settings

import os
import time
import varial.generators as gen
import varial.rendering as rnd
import varial.tools

def add_wrp_info_stacksig(wrps):
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path.split('/')[0],
        legend=lambda w: w.sample,
        is_signal=lambda w: w.sample == 'TpTp_M1000',
    )

def loader_hook(wrps):
    wrps = add_wrp_info_stacksig(wrps)
    wrps = gen.sort(wrps)
    # wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    return wrps


def plotter_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)


