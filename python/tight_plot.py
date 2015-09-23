#!/usr/bin/env python

import common_vlq
import common_plot
import settings
import sys

import os
import time
import varial.tools
import varial.generators as gen
from varial.sample import Sample
import varial.analysis as analysis
import normplots
import stackplots
import stackplots_sig
import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# if len(sys.argv) > 1:
#     target_dir = sys.argv[1]
#     if not target_dir.endswith('/'):
#         target_dir += '/'
# else:
#     target_dir = ''

# varial.settings.use_parallel_chains = False

# normfactors = {
#     'TpTp_M-700' : 20./0.455,
#     'TpTp_M-800' : 20./0.196,
#     'TpTp_M-900' : 20./0.0903,
#     'TpTp_M-1000' : 20./0.0440,
#     'TpTp_M-1100' : 20./0.0224,
#     'TpTp_M-1200' : 20./0.0118,
#     'TpTp_M-1300' : 20./0.00639,
#     'TpTp_M-1400' : 20./0.00354,
#     'TpTp_M-1500' : 20./0.00200,
#     'TpTp_M-1600' : 20./0.001,
#     'TpTp_M-1700' : 20./0.0005,
#     'TpTp_M-1800' : 20./0.00025,
# }

def only_tptp(filename):
    return not ('BpJ' in filename or 'TpJ' in filename)

# legend_preselection = {
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',

# }

def file_stack_all():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_stack_all_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and
            ('M1000_' not in f or any(w in f for w in [
                'thth',
                'thtz',
                'thbw',
                'bwbw',
                'tzbw',
                'tztz'
                ])
            )
            # and 'HT' not in f
        )]
    return file_stack_all_list

def file_stack_th():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_stack_th_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and
            ('M1000_' not in f or any(w in f and 'onelep' not in f for w in [
                'thth',
                'thtz',
                'thbw'
                ])
            )
            # and 'HT' not in f
        )]
    return file_stack_th_list

def file_stack_noth():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_stack_noth_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and
            ('M1000_' not in f or any(w in f for w in [
                'tztz',
                'tzbw',
                'bwbw'
                ])
            )
            # and 'HT' not in f
        )]
    return file_stack_noth_list

def file_stack_thonelep():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_stack_thonelep_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and
            ('M1000_' not in f or 'onelep' in f)
            # and 'HT' not in f
        )]
    return file_stack_thonelep_list

final_dir = 'Plots'

def mk_cutflow_chain_cr(category, loader_hook):
    cutflow_histos = varial.tools.HistoLoader(
        name='CutflowHistos',
        # pattern=input_pat,
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
                       category == w.in_file_path.split('/')[0],
        hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
    )

    cutflow_stack_plots = varial.tools.Plotter(
        'CutflowStack',
        stack=True,
        input_result_path='../CutflowHistos',
        save_log_scale=True,
        canvas_decorators=[varial.rendering.Legend]
    )

    # cutflow_normed_plots = varial.tools.Plotter(
    #     'CutflowNormed',
    #     stack=False,
    #     plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
    #     hook_loaded_histos=gen.gen_norm_to_max_val,
    #     input_result_path='../CutflowHistos',
    #     save_log_scale=True,
    #     canvas_decorators=[varial.rendering.Legend]
    # )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        cutflow_stack_plots,
        # cutflow_normed_plots,
        cutflow_tables.CutflowTableContent(),
        cutflow_tables.CutflowTableTxt(),
        cutflow_tables.CutflowTableTex(None, True),
    ])

def mk_tools_cr(categories=None):
    def create():
        plot_chain = [
            
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_stack_all_unsplit(),
                name='StackedAll',
                plotter_factory=lambda **w: stackplots.plotter_factory(common_plot.normfactors, **w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_no_signals(),
                name='NormedNoSignals',
                plotter_factory=lambda **w: normplots.plotter_factory(**w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_split_signals(),
                name='NormedSignals',
                plotter_factory=lambda **w: normplots.plotter_factory(**w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            
            ]
        cutflow_cat = []
        for cat in categories:
            cutflow_cat.append(mk_cutflow_chain_cr(
                cat,
                stackplots.loader_hook))
        plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_stack_all_unsplit(),
            name='StackedAll',
            plotter_factory=lambda **w: stackplots.plotter_factory(common_plot.normfactors, **w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_no_signals(),
            name='NormedNoSignals',
            plotter_factory=lambda **w: normplots.plotter_factory(**w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_split_signals(),
            name='NormedSignals',
            plotter_factory=lambda **w: normplots.plotter_factory(**w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        cutflow_tables.mk_cutflow_chain(common_plot.file_stack_all_unsplit(), stackplots.loader_hook)
        ]

if __name__ == '__main__':
    time.sleep(1)
    all_tools = mk_tools()
    tc = varial.tools.ToolChain(
        final_dir, all_tools)
    varial.tools.Runner(tc)
    # varial.tools.WebCreator(no_tool_check=True).run()   
    for itool in all_tools:
        dir_name = os.path.join('./'+final_dir, itool.name)
        print dir_name
        varial.tools.WebCreator(working_dir=dir_name).run()
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()

# working_dir='NormedSignal'

