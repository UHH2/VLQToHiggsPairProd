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
import common_sframe 

# varial.settings.use_parallel_chains = False


#====PLOTTING====

datasets_to_plot = [
    'Run2015D',
    'TpTp_M-800',
    'TpTp_M-1000',
    'TpTp_M-1200',
    'TpTp_M-1400',
    'TpTp_M-1600',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleT',
]

test_list = [
            'uhh2.AnalysisModuleRunner.MC.QCD_Pt1000toInf_MuEnr.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-1600.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-1000.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-800.root'
            ]

def mk_cutflow_chain_cat(category, loader_hook):
    cutflow_histos = varial.tools.HistoLoader(
        name='CutflowHistos',
        pattern=common_plot.file_select(datasets_to_plot),
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
                       category == w.in_file_path.split('/')[0],
        # hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
        hook_loaded_histos=lambda w: loader_hook(w)
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
        cutflow_tables.CutflowTableTex(None, True),
    ])

def plotter_factory_loose(**kws):
    # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: common_plot.loader_hook_norm_smpl(w, common_plot.normfactors)
    kws['plot_setup'] = common_plot.stack_setup_norm_sig
    kws['stack_setup'] = common_plot.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)

def mk_tools_cats(src='', categories=None):
    def create():
        plot_chain = [
            
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_select(datasets_to_plot, src),
                name='StackedAll',
                # filter_keyfunc=filter_for_fsp,
                # plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                plotter_factory=plotter_factory_loose,
                combine_files=True,
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
        cutflow_cat = []
        for cat in categories:
            cutflow_cat.append(mk_cutflow_chain_cat(
                cat,
                common_plot.loader_hook))
        plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create


#====SFRAME====

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_9/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

def mk_sframe_and_plot_tools(version='TestLoose', count=-1, allowed_datasets=None):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_datasets_eventnumber_and_split_loose(count=count, allowed_datasets=allowed_datasets), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_tools
    )
    tc = varial.tools.ToolChain(
        version,
        [
            sframe,
            plots,
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

def hadd_and_plot(version='Test', src='', categories=None):
    hadd = Hadd(
        src_glob_path='../../'+src,
        basenames=list('uhh2.AnalysisModuleRunner.MC.'+f for f in ['QCD', 'MC_WJets', 'DYJetsToLL', 'SingleT']), 
        )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_tools_cats(categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            hadd,
            plots,
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()

import sys

categories = ["IsoMuo24", "Mu45", "Mu15_PFHT600", "PFHT800"]

if __name__ == '__main__':
    time.sleep(1)
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    all_tools = hadd_and_plot(version=final_dir, src=src_dir, categories=categories)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.WebCreator(no_tool_check=True).run()   
    # for itool in all_tools:
    #     dir_name = os.path.join('./'+final_dir, itool.name)
    #     print dir_name
    #     varial.tools.WebCreator(working_dir=dir_name).run()
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()