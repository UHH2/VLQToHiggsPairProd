#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy

import varial.settings
import varial.tools
import varial.generators as gen
import varial.rendering as rnd
# import varial.analysis as analysis
# from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import plot_new as plot
import common_plot_new as common_plot
# import tptp_sframe 
# import compare_crs
import analysis

from ROOT import TLatex, TH2

def plot_grouper_sep_sig_bkg(wrps):
    # if separate_th2:
    #     wrps = rename_th2(wrps)
    return gen.group(wrps, key_func=lambda w: str(w.is_signal)+'___'+w.in_file_path)

def loader_hook_eff(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = plot.common_loader_hook(wrps)
    # wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    # wrps = gen.gen_make_th2_projections(wrps)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # # if varial.settings.merge_decay_channels:
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False)
        # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    # wrps = itertools.ifilter(lambda w: not any(w.sample.endswith(g) for g in ['_other']), wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: str(w.is_signal)+'___'+w.in_file_path)
    return wrps

def plotter_factory_eff():
	def mk_name(wrp):
		if wrp._renderers[0].is_signal:
			return 'sig_'
		else:
			return 'bkg_'
	
	def tmp(**kws):
	    # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
	    # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
	    kws['hook_loaded_histos'] = loader_hook_eff
	    kws['plot_grouper'] = plot_grouper_sep_sig_bkg
	    # kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
	    # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
	    # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
	    # kws['y_axis_scale'] = 'lin'
	    # kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
	    # kws['hook_canvas_post_build'] = canvas_setup_post
	    # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
	    kws['save_name_func'] = lambda w: mk_name(w)+w.name
	    kws['canvas_post_build_funcs'] = common_plot.get_style()
	    kws['mod_log'] = common_plot.mod_log_usr()
	    return varial.tools.Plotter(stack=False, **kws)
	return tmp


def plot_only(version='Test', pattern=''):
    plots = varial.tools.ToolChain(
        'Plots',
        lazy_eval_tools_func=plot.mk_plots(pattern=pattern, web_create=True, plotter_factory=plotter_factory_eff())
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots
        ]
    )
    return tc

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    all_tools = plot_only(version=final_dir, pattern=src_dir)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()