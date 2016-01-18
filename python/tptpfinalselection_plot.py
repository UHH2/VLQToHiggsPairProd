#!/usr/bin/env python

import sys
import os
import time

import varial.settings
import varial.tools
import varial.generators as gen
import varial.analysis as analysis
from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
import final_plotting
import common_plot
# import tptp_sframe 
import sensitivity
import compare_crs

# varial.settings.max_num_processes = 1


#====PLOTTING====

datasets_to_plot = [
    'Run2015D',
    # 'TpTp_M-800_thX',
    # 'TpTp_M-1000_thX',
    'TpTp_M-800',
    'TpTp_M-1200',
    # 'TpTp_M-1200_other',
    # 'TpTp_M-1400_thX',
    # 'TpTp_M-1600_thX',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'ST',
]

def add_fs_info(wrps):
    for w in wrps:
        w.finalstate = w.in_file_path.split('/')[0]
        w.in_file_path = '/'.join(w.in_file_path.split('/')[1:])
        yield w

def mk_cutflow_chain_cat(category, loader_hook):
    cutflow_histos = varial.tools.HistoLoader(
        name='CutflowHistos',
        # pattern=common_plot.file_select(datasets_to_plot),
        # input_result_path='../../../../HistoLoader',
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
                       category == w.in_file_path.split('/')[0],
        # hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
        # hook_loaded_histos=loader_hook
    )

    cutflow_stack_plots = varial.tools.Plotter(
        'CutflowStack',
        stack=True,
        input_result_path='../CutflowHistos',
        save_log_scale=True,
        canvas_decorators=[varial.rendering.Legend]
    )

    cutflow_normed_plots = varial.tools.Plotter(
        'CutflowNormed',
        # stack=False,
        plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
        hook_loaded_histos=gen.gen_norm_to_max_val,
        input_result_path='../CutflowHistos',
        # plot_setup=varial.plotter.default_plot_colorizer,
        save_lin_log_scale=True,
        canvas_decorators=[varial.rendering.Legend]
    )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        cutflow_normed_plots,
        cutflow_stack_plots,
        cutflow_tables.CutflowTableContent(),
        cutflow_tables.CutflowTableTxt(),
        # cutflow_tables.CutflowTableTex(None, True),
    ])

def loader_hook_finalstates_incl(wrps):
    wrps = common_plot.loader_hook_norm_smpl(wrps, common_plot.normfactors)
    wrps = gen.gen_add_wrp_info(
        wrps,
        finalstate = lambda w: w.in_file_path.split('/')[0],
        # variable=lambda w: w.in_file_path.split('/')[-1]
        )
    wrps = gen.gen_add_wrp_info(
        wrps,
        in_file_path = lambda w: '/'.join(w.in_file_path.split('/')[1:]),
        # variable=lambda w: w.in_file_path.split('/')[-1]
        )
    wrps = gen.sort(wrps, ['sample', 'in_file_path'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    wrps = common_plot.merge_finalstates_channels(wrps, ['_thth', '_thtz', '_thbw'], '_thX', True)
    wrps = common_plot.merge_finalstates_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], '_other', True)
    return wrps

def loader_hook_finalstates_excl(wrps):
    wrps = common_plot.loader_hook_norm_smpl(wrps, common_plot.normfactors)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], '_thX', True)
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], '_other', True)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def plotter_factory(**kws):
    # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
    # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
    kws['hook_loaded_histos'] = loader_hook_finalstates_excl
    kws['plot_setup'] = common_plot.stack_setup_norm_sig
    kws['stack_setup'] = common_plot.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)

def mk_plots_and_cf(src='../Hadd/*.root', categories=None):
    def create():
        plot_chain = [
            
            varial.plotter.RootFilePlotter(
                pattern=src,
                # input_result_path='../HistoLoader',
                name='StackedAll',
                filter_keyfunc=lambda w: any(f in w.sample for f in datasets_to_plot) and 'noH' not in w.sample,
                # plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                plotter_factory=plotter_factory,
                # combine_files=True,
                auto_legend=False
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            
            ]
        if categories:
            cutflow_cat = []
            for cat in categories:
                cutflow_cat.append(mk_cutflow_chain_cat(
                    cat,
                    None))
            plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_toolchain(name='', src='', categories=None):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories)
        )

def hadd_and_plot(version='Test', src='', categories=None):
    hadd = Hadd(
        src_glob_path='../../'+src,
        basenames=common_plot.basenames, 
        )
    # histo_loader = varial.tools.HistoLoader(
    #     # name='CutflowHistos',
    #     pattern='../Hadd/*.root',
    #     filter_keyfunc=lambda w: w.type.startswith('TH1')\
    #      and any(f in w.sample for f in datasets_to_plot),
    #     # filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
    #     #                category == w.in_file_path.split('/')[1],
    #     # hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
    #     hook_loaded_histos=loader_hook_finalstates_excl
    # )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_plots_and_cf(categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            hadd,
            # histo_loader,
            plots,
            # varial.tools.ToolChainParallel(
            #     'CompareControlRegions',
            #     lazy_eval_tools_func=compare_crs.mk_tc(srs=list(c for c in categories if 'Signal' in c),
            #             crs=list(c for c in categories if 'Control' in c))
            #     ),
            # sensitivity.mk_tc('Limits'),
            # varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()

import sys
import tptpsframe_runner as sframe

if __name__ == '__main__':
    time.sleep(1)
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    all_tools = hadd_and_plot(version=final_dir, src=src_dir, categories=sframe.categories)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()