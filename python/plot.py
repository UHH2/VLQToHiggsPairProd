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
import varial.analysis as analysis
from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot
# import tptp_sframe 
import sensitivity
import compare_crs

from ROOT import TLatex, TH2

# varial.settings.max_num_processes = 1

#====PLOTTING====

#====DEFINITIONS====

src_dir_rel = '../Hadd'

normsignal = 20.

basenames_final = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015CD',
    'DATA.SingleEle_Run2015CD',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TpTp_M-0700_thth', 'MC.TpTp_M-0700_thtz', 'MC.TpTp_M-0700_thbw', 'MC.TpTp_M-0700_noH_tztz', 'MC.TpTp_M-0700_noH_tzbw', 'MC.TpTp_M-0700_noH_bwbw',
    'MC.TpTp_M-0800_thth', 'MC.TpTp_M-0800_thtz', 'MC.TpTp_M-0800_thbw', 'MC.TpTp_M-0800_noH_tztz', 'MC.TpTp_M-0800_noH_tzbw', 'MC.TpTp_M-0800_noH_bwbw',
    'MC.TpTp_M-0900_thth', 'MC.TpTp_M-0900_thtz', 'MC.TpTp_M-0900_thbw', 'MC.TpTp_M-0900_noH_tztz', 'MC.TpTp_M-0900_noH_tzbw', 'MC.TpTp_M-0900_noH_bwbw',
    'MC.TpTp_M-1000_thth', 'MC.TpTp_M-1000_thtz', 'MC.TpTp_M-1000_thbw', 'MC.TpTp_M-1000_noH_tztz', 'MC.TpTp_M-1000_noH_tzbw', 'MC.TpTp_M-1000_noH_bwbw',
    'MC.TpTp_M-1100_thth', 'MC.TpTp_M-1100_thtz', 'MC.TpTp_M-1100_thbw', 'MC.TpTp_M-1100_noH_tztz', 'MC.TpTp_M-1100_noH_tzbw', 'MC.TpTp_M-1100_noH_bwbw',
    'MC.TpTp_M-1200_thth', 'MC.TpTp_M-1200_thtz', 'MC.TpTp_M-1200_thbw', 'MC.TpTp_M-1200_noH_tztz', 'MC.TpTp_M-1200_noH_tzbw', 'MC.TpTp_M-1200_noH_bwbw',
    'MC.TpTp_M-1300_thth', 'MC.TpTp_M-1300_thtz', 'MC.TpTp_M-1300_thbw', 'MC.TpTp_M-1300_noH_tztz', 'MC.TpTp_M-1300_noH_tzbw', 'MC.TpTp_M-1300_noH_bwbw',
    'MC.TpTp_M-1400_thth', 'MC.TpTp_M-1400_thtz', 'MC.TpTp_M-1400_thbw', 'MC.TpTp_M-1400_noH_tztz', 'MC.TpTp_M-1400_noH_tzbw', 'MC.TpTp_M-1400_noH_bwbw',
    'MC.TpTp_M-1500_thth', 'MC.TpTp_M-1500_thtz', 'MC.TpTp_M-1500_thbw', 'MC.TpTp_M-1500_noH_tztz', 'MC.TpTp_M-1500_noH_tzbw', 'MC.TpTp_M-1500_noH_bwbw',
    'MC.TpTp_M-1600_thth', 'MC.TpTp_M-1600_thtz', 'MC.TpTp_M-1600_thbw', 'MC.TpTp_M-1600_noH_tztz', 'MC.TpTp_M-1600_noH_tzbw', 'MC.TpTp_M-1600_noH_bwbw',
    'MC.TpTp_M-1700_thth', 'MC.TpTp_M-1700_thtz', 'MC.TpTp_M-1700_thbw', 'MC.TpTp_M-1700_noH_tztz', 'MC.TpTp_M-1700_noH_tzbw', 'MC.TpTp_M-1700_noH_bwbw',
    'MC.TpTp_M-1800_thth', 'MC.TpTp_M-1800_thtz', 'MC.TpTp_M-1800_thbw', 'MC.TpTp_M-1800_noH_tztz', 'MC.TpTp_M-1800_noH_tzbw', 'MC.TpTp_M-1800_noH_bwbw',
    ])

basenames_pre = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015CD',
    'DATA.SingleEle_Run2015CD',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TpTp_M-0700',
    'MC.TpTp_M-0800',
    'MC.TpTp_M-0900',
    'MC.TpTp_M-1000',
    'MC.TpTp_M-1100',
    'MC.TpTp_M-1200',
    'MC.TpTp_M-1300',
    'MC.TpTp_M-1400',
    'MC.TpTp_M-1500',
    'MC.TpTp_M-1600',
    'MC.TpTp_M-1700',
    'MC.TpTp_M-1800',
    ])

normfactors = {
    # 'TpTp' : 20.,
    '_thX' : 1./0.56,
    '_other' : 1./0.44,
    'TpTp_M-0700' : 1./0.455,
    'TpTp_M-0800' : 1./0.196,
    'TpTp_M-0900' : 1./0.0903,
    'TpTp_M-1000' : 1./0.0440,
    'TpTp_M-1100' : 1./0.0224,
    'TpTp_M-1200' : 1./0.0118,
    'TpTp_M-1300' : 1./0.00639,
    'TpTp_M-1400' : 1./0.00354,
    'TpTp_M-1500' : 1./0.00200,
    'TpTp_M-1600' : 1./0.001148,
    'TpTp_M-1700' : 1./0.000666,
    'TpTp_M-1800' : 1./0.000391,
}


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
    'Run2015CD',
]

samples_to_plot_final = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in signals_to_plot))

samples_to_plot_pre = other_samples_to_plot + signals_to_plot

get_samplename = vlq_common.get_samplename

varial.settings.pretty_names.update({
    'no sel._tex' : 'no sel.',
    'trigger_accept_el45_tex' : 'trigger',
    'trigger_accept_mu45_tex' : 'trigger',
    'primary_lepton_pt_tex' : 'pt(Lepton)',
    'primary_electron_pt_tex' : 'pt(Electron)',
    'primary_muon_pt_tex' : 'pt(Muon)',
    'pt_ld_ak4_jet_tex' : 'pt(1st AK4 jet)',
    'pt_subld_ak4_jet_tex' : 'pt(2nd AK4 jet)',
    '2D cut_tex' : '2D cut',
    'ST_tex' : 'ST',
    'n_ak8_tex' : 'N(AK8-jets)',
    'pt_ld_ak8_jet_tex' : 'pt(1st AK8 jet)',
} )


def common_loader_hook(wrps):
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = common_plot.mod_legend(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    return wrps

#=======FOR CUTFLOWS=======

def cf_loader_hook(wrps):
    wrps = common_loader_hook(wrps)
    wrps = cutflow_tables.rebin_cutflow(wrps)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    #=== FIX MERGING WITH PREFIXES===
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=None, prefixes=['SingleMuon_', 'SingleEle_'], print_warning=False)
    if varial.settings.merge_decay_channels:
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def mk_cutflow_chain_cat(category, loader_hook, datasets):
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


#=======FOR ALL PLOTS=======





def loader_hook_finalstates_excl(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = common_plot.mod_bin(wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, normfactors)
    wrps = gen.gen_make_th2_projections(wrps)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # for w in wrps: print w.sample, w.in_file_path
    if varial.settings.merge_decay_channels:
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
        wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = common_plot.mod_legend(wrps)
    wrps = common_plot.mod_title(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps



def loader_hook_norm_to_int(wrps):
    key = lambda w: '{0}___{1}___{2}___{3}'.format(w.in_file_path, w.is_data, w.is_signal if not w.is_signal else w.sample, w.sys_info)

    wrps = loader_hook_finalstates_excl(wrps)
    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = common_plot.norm_to_int(wrps)
    return wrps

# def mk_legend_bkg(wrps):
#     for w in wrps:
#         if not w.is_signal and not w.is_data:
#             w.legend = ""

# def loader_hook_gen_reco_ht_comp(wrps):
#     key = lambda w: '{0}___{1}___{2}___{3}'.format(w.in_file_path, w.is_data, w.is_signal if not w.is_signal else w.sample, w.sys_info)

#     wrps = loader_hook_finalstates_excl(wrps)
#     wrps = sorted(wrps, key=key)
#     wrps = varial.gen.group(wrps, key)
#     wrps = varial.gen.gen_merge(wrps)
#     wrps = mk_legend_bkg(wrps)
#     return wrps

def loader_hook_uncerts(wrps):
    def set_line_width(wrps):
        for w in wrps:
            if isinstance(w, wrappers.HistoWrapper):
                w.histo.SetLineWidth(2)
            yield w

    wrps = loader_hook_finalstates_excl(wrps)
    wrps = set_line_width(wrps)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    return wrps


def group_by_uncerts(wrps, first_sort_func):
    def sort_key_func(wrp):
        if wrp.sys_info:
            return wrp.sys_info.split('__')[0]
        else:
            return ''

    wrps = itertools.groupby(wrps, first_sort_func)
    for k1, g in wrps:
        g = sorted(g, key=sort_key_func)
        g = list(g)
        nominal = g[0]
        sys_uncerts = itertools.groupby(g[1:], sort_key_func)
        for k2, sys in sys_uncerts:
            # print nominal.in_file_path, nominal.sample, nominal.sys_info, list((s.in_file_path, s.sample, s.sys_info) for s in sys)
            nom_copy = copy.copy(nominal)
            nom_copy.name = nom_copy.name+'__'+nom_copy.sample+'__'+k2
            yield wrappers.WrapperWrapper([nom_copy]+list(sys), name=k1+'__'+k2)

# def group_gen_reco_ht(wrps):

#     wrps = itertools.groupby(wrps, first_sort_func)
#     for k1, g in wrps:
#         g = sorted(g, key=lambda w: '{0}'.format())
#         g = list(g)
#         nominal = g[0]
#         sys_uncerts = itertools.groupby(g[1:], sort_key_func)
#         for k2, sys in sys_uncerts:
#             # print nominal.in_file_path, nominal.sample, nominal.sys_info, list((s.in_file_path, s.sample, s.sys_info) for s in sys)
#             nom_copy = copy.copy(nominal)
#             nom_copy.name = nom_copy.name+'__'+nom_copy.sample+'__'+k2
#             yield wrappers.WrapperWrapper([nom_copy]+list(sys), name=k1+'__'+k2)

def plot_setup_uncerts(grps):
    def set_legend(wrps):
        for w in wrps:
            if not w.sys_info:
                w.legend = 'nominal'
            else:
                w.legend = w.sys_info.split('__')[1]
            yield w

    grps = (set_legend(ws) for ws in grps)
    grps = varial.plotter.default_plot_colorizer(grps)
    return grps


def stack_setup_norm_sig(grps):
    grps = gen.mc_stack_n_data_sum(grps)
    if varial.settings.flex_sig_norm:
        grps = common_plot.norm_to_bkg(grps)
    return grps

def stack_setup_norm_all_to_intgr(grps):
    grps = gen.mc_stack_n_data_sum(grps)
    grps = common_plot.norm_stack_to_integral(grps)
    return grps

def plotter_factory_stack(**args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_finalstates_excl
        kws['plot_setup'] = stack_setup_norm_sig
        kws['stack_setup'] = stack_setup_norm_sig
        # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        kws['save_lin_log_scale'] = True
        kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        kws['canvas_decorators'] = [varial.rendering.BottomPlotRatioSplitErr,
            varial.rendering.Legend,
            # varial.rendering.TextBox(textbox=TLatex(0.5, 0.5, "My Box"))
            ]
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp


def plotter_factory_uncerts(**args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_uncerts
        kws['plot_grouper'] = lambda w: group_by_uncerts(w, 
            lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
        kws['plot_setup'] = plot_setup_uncerts
        # kws['stack_setup'] = stack_setup_norm_sig
        # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        kws['save_lin_log_scale'] = True
        # kws['save_name_func'] = lambda w: w.save_name
        kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        kws['canvas_decorators'] = [varial.rendering.BottomPlotRatioSplitErr,
            varial.rendering.Legend,
            # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
            ]
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp

def mk_plots_and_cf(src='../Hadd/*.root', categories=None, datasets=samples_to_plot_pre, filter_keyfunc=None, **kws):
    if filter_keyfunc:
        filter_func = filter_keyfunc 
    else:
        filter_func = lambda w: any(f in w.file_path.split('/')[-1] for f in datasets)
    def create():
        plot_chain = [
            
            varial.plotter.RootFilePlotter(
                pattern=src,
                # input_result_path='../HistoLoader',
                name='StackedAll',
                filter_keyfunc=filter_func, #and 'noH' not in w.sample,
                # filter_keyfunc=lambda w: any(f in w.sample for f in datasets_to_plot) and 'noH' not in w.sample,
                # plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                plotter_factory=plotter_factory_stack(**kws),
                # combine_files=True,
                auto_legend=False
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            varial.plotter.RootFilePlotter(
                pattern=src,
                # input_result_path='../HistoLoader',
                name='CompareUncerts',
                filter_keyfunc=lambda w: any(f in w.file_path for f in ['TTbar', 'WJets']) and w.in_file_path.endswith('ST'), #and 'noH' not in w.sample,
                # filter_keyfunc=lambda w: any(f in w.sample for f in datasets_to_plot) and 'noH' not in w.sample,
                # plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                plotter_factory=plotter_factory_uncerts(**kws),
                # combine_files=True,
                auto_legend=False
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            # varial.tools.Plotter(
            #     'GenRecoHTComparisons',
            #     stack=True,
            #     input_result_path='../CutflowHistos',
            #     save_log_scale=True,
            #     canvas_decorators=[varial.rendering.Legend]
            #     )
            
            ]
        if categories:
            cutflow_cat = []
            for cat in categories:
                if cat is not 'NoSelection' and cat is not 'CombinedElMu':
                    cutflow_cat.append(mk_cutflow_chain_cat(
                        cat,
                        common_loader_hook,
                        datasets))
            plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_toolchain(name, src, datasets, categories=None, filter_keyfunc=None):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories, datasets=datasets, filter_keyfunc=filter_keyfunc)
        )

def mk_toolchain_pull(name, src, datasets, categories=None, filter_keyfunc=None):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories, datasets=datasets, filter_keyfunc=filter_keyfunc, 
            canvas_decorators=[varial.rendering.BottomPlotRatioPullErr,
                varial.rendering.Legend,
                # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                ])
        )

def mk_toolchain_norm(name, src, datasets, categories=None, filter_keyfunc=None):
    # varial.settings.do_norm_plot = True
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories, datasets=datasets, filter_keyfunc=filter_keyfunc, hook_loaded_histos=loader_hook_norm_to_int)
        )

def mk_toolchain_norm_pull(name, src, datasets, categories=None, filter_keyfunc=None):
    # varial.settings.do_norm_plot = True
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories, datasets=datasets, filter_keyfunc=filter_keyfunc, hook_loaded_histos=loader_hook_norm_to_int,
            canvas_decorators=[varial.rendering.BottomPlotRatioPullErr,
                varial.rendering.Legend,
                # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                ])
        )

import tex_content

def plot_only(version='Test', src='', categories=None):
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_plots_and_cf(src=src, categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots,
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
    varial.tools.Runner(all_tools, default_reuse=False)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()