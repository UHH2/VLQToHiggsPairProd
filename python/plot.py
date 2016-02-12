#!/usr/bin/env python

import sys
import os
import time

import varial.settings
import varial.tools
import varial.generators as gen
import varial.rendering as rnd
import varial.analysis as analysis
from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
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
    'TpTp_M-0700',
    # 'TpTp_M-0800',
    # 'TpTp_M-0900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    # 'TpTp_M-1700',
    'TpTp_M-1800',
    # 'TpTp_M-1200_other',
    # 'TpTp_M-1400_thX',
    # 'TpTp_M-1600_thX',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleTop',
]



signals_to_plot = [
    'TpTp_M-0700',
    # 'TpTp_M-0800',
    # 'TpTp_M-0900',
    'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    'TpTp_M-1700',
    # 'TpTp_M-1800',
]

final_states_to_plot = [
    '_thth',
    '_thtz',
    '_thbw',
    # '_noH_tztz',
    # '_noH_tzbw',
    # '_noH_bwbw',
]

other_samples_to_plot = [
    'TTbar',
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015D',
]

samples_to_plot_final = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in signals_to_plot))

samples_to_plot_pre = other_samples_to_plot + signals_to_plot

def add_fs_info(wrps):
    for w in wrps:
        w.finalstate = w.in_file_path.split('/')[0]
        w.in_file_path = '/'.join(w.in_file_path.split('/')[1:])
        yield w

varial.settings.pretty_names.update({
    'no sel._tex' : 'no sel.',
    'trigger_accept_el45_tex' : 'trigger',
    'primary_lepton_pt_tex' : 'pt(Lepton)',
    'pt_ld_ak4_jet_tex' : 'pt(1st AK4 jet)',
    'pt_subld_ak4_jet_tex' : 'pt(2nd AK4 jet)',
    '2D cut_tex' : '2D cut',
    'ST_tex' : 'ST',
    'n_ak8_tex' : 'N(AK8-jets)',
    'pt_ld_ak8_jet_tex' : 'pt(1st AK8 jet)',
} )

# def mod_cf_label(wrps):
#     for wrp in wrps:
#         for i in xrange(wrp.histo.GetNbinsX()):
#             bin_label = cutflow_names.get(wrp.histo.GetXaxis().GetBinLabel(i + 1))
#             if bin_label:
#                 wrp.histo.GetXaxis().SetBinLabel(i + 1, bin_label)
#         yield wrp

def cf_loader_hook(wrps):
    wrps = common_plot.loader_hook(wrps)
    wrps = cutflow_tables.rebin_cutflow(wrps)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    #=== FIX MERGING WITH PREFIXES===
    wrps = vlq_common.merge_decay_channels(wrps, postfixes=None, prefixes=['SingleMuon_', 'SingleEle_'], print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def mk_cutflow_chain_cat(category, loader_hook, datasets=datasets_to_plot):
    cutflow_histos = varial.tools.HistoLoader(
        pattern='../../../../Hadd/*.root',
        name='CutflowHistos',
        # pattern=common_plot.file_select(datasets_to_plot),
        # input_result_path='../../../../HistoLoader',
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1]\
                       and category == w.in_file_path.split('/')[0] \
                       and any(f in w.file_path for f in datasets),
                       # and (('SingleEle' not in w.file_path and 'Mu' in category) or\
                       # ('SingleMuon' not in w.file_path and 'El' in category)),
        # hook_loaded_histos=lambda w: cutflow_tables.rebin_cutflow(loader_hook(w))
        hook_loaded_histos=cf_loader_hook
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
    #     # stack=False,
    #     plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
    #     hook_loaded_histos=gen.gen_norm_to_max_val,
    #     input_result_path='../CutflowHistos',
    #     # plot_setup=varial.plotter.default_plot_colorizer,
    #     save_lin_log_scale=True,
    #     canvas_decorators=[varial.rendering.Legend]
    # )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        # cutflow_normed_plots,
        cutflow_stack_plots,
        cutflow_tables.CutflowTableContent(),
        cutflow_tables.CutflowTableTxt(),
        cutflow_tables.CutflowTableTex(True, None),
    ])

# def loader_hook_finalstates_incl(wrps):
#     wrps = common_plot.loader_hook_norm_smpl(wrps, common_plot.normfactors)
#     wrps = gen.gen_add_wrp_info(
#         wrps,
#         finalstate = lambda w: w.in_file_path.split('/')[0],
#         # variable=lambda w: w.in_file_path.split('/')[-1]
#         )
#     wrps = gen.gen_add_wrp_info(
#         wrps,
#         in_file_path = lambda w: '/'.join(w.in_file_path.split('/')[1:]),
#         # variable=lambda w: w.in_file_path.split('/')[-1]
#         )
#     wrps = gen.sort(wrps, ['sample', 'in_file_path'])
#     # wrps = list(wrps)
#     # for w in wrps: print w.sample, w.in_file_path 
#     wrps = common_plot.merge_finalstates_channels(wrps, ['_thth', '_thtz', '_thbw'], '_thX', True)
#     wrps = common_plot.merge_finalstates_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], '_other', True)
#     return wrps

def loader_hook_norm_smpl(wrps, smpl_fct=None, rebin_max_bins=60):
    if rebin_max_bins:
        wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, rebin_max_bins)
    wrps = common_plot.loader_hook(wrps)
    # wrps = gen.sort(wrps, key_list=['in_file_path', 'sample'])
    wrps = common_plot.norm_smpl(wrps, smpl_fct)
    wrps = gen.gen_make_th2_projections(wrps)
    return wrps

def loader_hook_finalstates_excl(wrps):
    wrps = loader_hook_norm_smpl(wrps, common_plot.normfactors, rebin_max_bins=60)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def add_sample_integrals(canvas_builders):
    """
    Adds {'legend1' : histo_integral, ...} to canvases.
    """
    def integral_histo_wrp(wrp):
        fct = 1.
        if hasattr(wrp, 'scl_fct'):
            fct = wrp.scl_fct
        return [(wrp.legend, wrp.obj.Integral()/fct)]

    def integral_stack_wrp(wrp):
        for hist in wrp.obj.GetHists():
            fct = 1.
            if hasattr(wrp, 'scl_fct'):
                fct = wrp.scl_fct
            yield hist.GetTitle(), hist.Integral()/fct

    def integral(wrp):
        if isinstance(wrp, rnd.StackRenderer):
            return integral_stack_wrp(wrp)
        else:
            return integral_histo_wrp(wrp)

    for cnv in canvas_builders:
        # TODO when rendering goes generator
        cnv.renderers[0].__dict__.update(dict(
            ('Integral___' + legend, integ)
            for r in cnv.renderers
            if isinstance(r, rnd.HistoRenderer)  # applies also to StackRnd.
            for legend, integ in integral(r)
        ))
        yield cnv

def plotter_factory(**kws):
    # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
    # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
    kws['hook_loaded_histos'] = loader_hook_finalstates_excl
    kws['plot_setup'] = common_plot.stack_setup_norm_sig
    kws['stack_setup'] = common_plot.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    kws['hook_canvas_post_build'] = add_sample_integrals
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)

def mk_plots_and_cf(src='../Hadd/*.root', categories=None, datasets=datasets_to_plot):
    def create():
        plot_chain = [
            
            varial.plotter.RootFilePlotter(
                pattern=src,
                # input_result_path='../HistoLoader',
                name='StackedAll',
                filter_keyfunc=lambda w: any(f in w.file_path for f in datasets), #and 'noH' not in w.sample,
                # filter_keyfunc=lambda w: any(f in w.sample for f in datasets_to_plot) and 'noH' not in w.sample,
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
                if cat is not 'NoSelection':
                    cutflow_cat.append(mk_cutflow_chain_cat(
                        cat,
                        common_plot.loader_hook,
                        datasets))
            plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_toolchain(name='', src='', categories=None, datasets=datasets_to_plot):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories, datasets=datasets)
        )

import tex_content

def hadd_and_plot(version='Test', src='', categories=None, basenames=None, datasets=datasets_to_plot):
    hadd = Hadd(
        src_glob_path='../../'+src,
        basenames=basenames, 
        # overwrite=False
        )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_plots_and_cf(categories=categories, datasets=datasets)
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
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

def plot_only(version='Test', src='', categories=None, basenames=None):
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            # histo_loader,
            plots,
            # varial.tools.ToolChainParallel(
            #     'CompareControlRegions',
            #     lazy_eval_tools_func=compare_crs.mk_tc(srs=list(c for c in categories if 'Signal' in c),
            #             crs=list(c for c in categories if 'Control' in c))
            #     ),
            # sensitivity.mk_tc('Limits'),
            varial.tools.WebCreator(no_tool_check=True)
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
    if len(sys.argv) >= 3:
        cats = sys.argv[3:]
    else:
        cats = None
    all_tools = plot_only(version=final_dir, src=src_dir, categories=cats)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()