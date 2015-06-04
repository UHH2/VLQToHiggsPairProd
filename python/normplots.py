#!/usr/bin/env python

import common_vlq
import settings

import os
import time
import varial.tools
import varial.generators as gen


def loader_hook(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    wrps = gen.switch(
        wrps,
        lambda w: w.in_file_path.split('/')[0] == 'GenHists',
        gen.gen_make_th2_projections
    )
    wrps = gen.gen_make_eff_graphs(wrps)
    wrps = gen.switch(
        wrps,
        lambda w: 'TH1' in w.type,
        gen.gen_noex_norm_to_integral
    )
    return wrps


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)

def loader_hook_cf(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    wrps = gen.sort(wrps)
    wrps = common_vlq.merge_samples(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    wrps = common_vlq.norm_histos_to_first_bin(wrps)
    return wrps

def plotter_factory_cf(**kws):
    kws['hook_loaded_histos'] = loader_hook
    kws['save_lin_log_scale'] = True
    return varial.tools.Plotter(**kws)




