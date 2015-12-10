#!/usr/bin/env python

import sys
import os
import time

import varial.settings
import varial.tools
import varial.generators as gen
import varial.analysis as analysis
from varial.sample import Sample
from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# import common_vlq
import tptp_settings
import final_plotting
import common_plot
import tptp_sframe 
import sensitivity
import compare_crs

# varial.settings.max_num_processes = 1


#====PLOTTING====

datasets_to_plot = [
    'SingleMuon',
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
        input_result_path='../../../../HistoLoader',
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

def loader_hook_loader(wrps):
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
    # for w in wrps: print w.sample, w.finalstate, w.in_file_path 
    wrps = common_plot.merge_finalstates_channels(wrps, ['thth', 'thtz', 'thbw'], '_thX', True)
    wrps = common_plot.merge_finalstates_channels(wrps, ['noH_tztz', 'noH_tzbw', 'noH_bwbw'], '_other', True)
    return wrps

def plotter_factory(**kws):
    # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
    # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
    kws['hook_loaded_histos'] = lambda w: gen.sort(w, ['in_file_path'])
    kws['plot_setup'] = common_plot.stack_setup_norm_sig
    kws['stack_setup'] = common_plot.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)

def mk_tools_cats(src='', categories=None):
    def create():
        plot_chain = [
            
            varial.plotter.RootFilePlotter(
                pattern=None,
                input_result_path='../HistoLoader',
                name='StackedAll',
                filter_keyfunc=lambda w: any(f in w.sample for f in datasets_to_plot) and 'other' not in w.sample,
                # plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                plotter_factory=plotter_factory,
                # combine_files=True,
                auto_legend=False
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            # varial.tools.mk_rootfile_plotter(
            #     pattern=common_plot.file_no_signals(),
            #     name='NormedNoSignals',
            #     plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            #     combine_files=True,
            #     # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            #     ),
            # varial.tools.mk_rootfile_plotter(
            #     pattern=common_plot.file_split_signals(),
            #     name='NormedSignals',
            #     plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            #     combine_files=True,
            #     # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            #     ),
            
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


#====SFRAME====

# sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_9/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

# def mk_sframe_and_plot_tools(version='TestLoose', count=-1, allowed_datasets=None):
#     """Makes a toolchain for one category with sframe and plots."""
#     sframe = SFrame(
#         cfg_filename=sframe_cfg,
#         xml_tree_callback=tptp_sframe.set_datasets_eventnumber_and_split_loose(count=count, allowed_datasets=allowed_datasets), # 
#     )
#     plots = varial.tools.ToolChainParallel(
#         'Plots',
#         lazy_eval_tools_func=mk_tools
#     )
#     tc = varial.tools.ToolChain(
#         version,
#         [
#             sframe,
#             plots,
#             varial.tools.WebCreator(no_tool_check=True)
#         ]
#     )
#     return tc

basenames = list('uhh2.AnalysisModuleRunner.'+f for f in ['DATA.SingleMuon_Run2015D', 'MC.MC_QCD', 'MC.MC_WJets', 'MC.MC_DYJetsToLL', 'MC.MC_ST', 'MC.MC_TTbar',
            'MC.MC_TpTp_M-800', 'MC.MC_TpTp_M-1000', 'MC.MC_TpTp_M-1200', 'MC.MC_TpTp_M-1400', 'MC.MC_TpTp_M-1600'])

def hadd_and_plot(version='Test', src='', categories=None):
    hadd = Hadd(
        src_glob_path='../../'+src,
        basenames=basenames, 
        )
    # histo_tc = varial.tools.ToolChain(
    #     'HistoLoader',
    #     [
    #         varial.tools.ToolChainParallel
    #     ])
    histo_loader = varial.tools.HistoLoader(
        # name='CutflowHistos',
        pattern='../Hadd/*.root',
        filter_keyfunc=lambda w: w.type.startswith('TH1')\
         and any(f in w.sample for f in datasets_to_plot),
        # filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
        #                category == w.in_file_path.split('/')[1],
        # hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
        hook_loaded_histos=loader_hook_loader
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_tools_cats(categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            hadd,
            histo_loader,
            plots,
            sensitivity.mk_tc('Limits'),
            varial.tools.ToolChainParallel(
                'CompareControlRegions',
                lazy_eval_tools_func=compare_crs.mk_tc(srs=list(c for c in categories if 'Signal' in c),
                        crs=list(c for c in categories if 'Control' in c))
                ),
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()

import sys

# categories = ["HiggsTag1b", "HiggsTag2b"]
categories = ["NoSelection",
        "HiggsTag0Med-Control", #"HiggsTag0Med-Control-2Ak8", "HiggsTag0Med-Control-3Ak8", "HiggsTag0Med-Control-4Ak8", 
        "HiggsTag1bMed-Signal", #"HiggsTag1bMed-Signal-1addB", "HiggsTag1bMed-Signal-2addB", "HiggsTag1bMed-Signal-3addB",
        "HiggsTag2bMed-Signal", 
        ]

if __name__ == '__main__':
    time.sleep(1)
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    all_tools = hadd_and_plot(version=final_dir, src=src_dir, categories=categories)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()