#!/usr/bin/env python

import sys
import os
import time
import math

import varial.settings
import varial.rendering as rnd
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
# import tptp_sframe 
# import compare_crs
import analysis
import sensitivity
import combination_limits
import tex_content_new as tex_content
from get_eff_count import CountTable, EffTable # EffNumTable, 

from ROOT import TLatex, TH2

hists_to_plot = [
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015CD',
    # 'Diboson'
    'TTbar_split'
]

less_signals_bb = [
    'BpBp_M-0800',
    'BpBp_M-1200',
    'BpBp_M-1600',
]

samples_to_plot_tt = hists_to_plot + list(g + '_thth' for g in plot.less_signals) + list(g + '_noH_bwbw' for g in plot.less_signals)
samples_to_plot_thth = hists_to_plot + list(g + '_thth' for g in plot.less_signals)
samples_to_plot_bwbw = hists_to_plot + list(g + '_noH_bwbw' for g in plot.less_signals)
samples_to_plot_bb = hists_to_plot + list(g + '_noH_twtw' for g in less_signals_bb)

# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24'
# source_dir = os.path.join(base_path, 
#     'Run8_withHighMassTTbarSample/RunAnalysis/NoReweighting/TreeProject')
base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'
source_dir = os.path.join(base_path, 
    'TreeProjectTest/NoReweightingCheck/TreeProject')
uncerts = analysis.all_uncerts + ['sfel_trg'] # or get_sys_dir()
nom_pattern_tt = [source_dir+'/TreeProjectorBkg/{0}.root', source_dir+'/TreeProjectorTT/{0}.root']
sys_pattern_tt = list(source_dir+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts) +\
                    list(source_dir+'/SysTreeProjectorsTT/%s*/{0}.root'% i for i in uncerts)
nom_pattern_bb = [source_dir+'/TreeProjectorBkg/{0}.root', source_dir+'/TreeProjectorBB/{0}.root']
sys_pattern_bb = list(source_dir+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts) +\
                    list(source_dir+'/SysTreeProjectorsBB/%s*/{0}.root'% i for i in uncerts)
input_pattern_tt = nom_pattern_tt+sys_pattern_tt
input_pattern_bb = nom_pattern_bb+sys_pattern_bb

common_plot.pas_normfactors = {}

common_plot.norm_reg_dict = {}

mod_dict = {

    ##### GENERAL VARIABLES ######
    'ST' : {
            'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'y_max_fct' : 1.2,
            'bin_width' : 100,
            'err_empty_bins' : True
            },
    'ST_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 2e-3,
            'bin_width' : 100,
            'set_leg_2_col_log' : {
                    'x_pos': 0.7,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'y_max_fct' : 1.8,
            # 'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },
    'HT' : {
            'rebin_list' : [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            },
    'HT_rebin_flex' : {
            'title' : 'H_{T} [GeV]',
            'y_max_fct' : 1000000,
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 1e-5,
            'bin_width' : 100,
            'set_leg_2_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'y_max_fct' : 1.8,
            'err_empty_bins' : True,
            'draw_x_errs' : True
            },
    'primary_lepton_pt' : {
            'rebin' : 25,
            'set_leg_2_col_log' : common_plot.leg_2_col_def,
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 0.1,
            'title' : 'Primary Lepton p_{T} [GeV]',
            },
    'met' : {
            'title' : 'missing E_{T} [GeV]',
            'rebin' : 30,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    }

plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt', 'nobtag_boost_mass_nsjbtags']

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(),
        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(mod_dict),
        common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
    ]



def merge_sig_data(wrps, print_warning=True):
    """histos must be sorted!!"""

    def do_merging(buf):
        if len(buf) > 2:
            raise RuntimeError('ERROR Need exactly two histograms (data+signal) to merge.')

        # buf = sorted(buf, key=lambda w: w.is_signal)
        res = varial.operations.merge(buf)
        res.file_path = ''
        # res.histo.Sumw2()
        for i in xrange(1, res.histo.GetNbinsX() + 1):
            err = math.sqrt(res.histo.GetBinContent(i))
            res.histo.SetBinError(i, err)
        del buf[:]
        return res

    buf = []
    for w in wrps:
        if w.is_data or w.is_signal:
            buf.append(w)
            if len(buf) == 2:
                yield do_merging(buf)
        else:
            if buf:
                if print_warning:
                    print 'WARNING In merge_sig_data: buffer not empty.\n' \
                          'Flushing remaining items:\n' + ' | '.join(
                        '%s, %s' % (w.sample, w.in_file_path) for w in buf
                    )
                yield do_merging(buf)
            yield w
    if buf:
        yield do_merging(buf)

def loader_hook_merge_sig_data(wrps):
    def sort_signal_data(wrp):
        if wrp.is_data:
            return '0'
        elif wrp.is_signal:
            return '1'
        else:
            return '2'

    wrps = common_plot.mod_title(wrps)
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.name+'___'+sort_signal_data(w))
    wrps = merge_sig_data(wrps, False)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'___'+w.name)
    return wrps

def mk_histoloader_merge(input_pattern, plot_hists=plot_hists, samples=samples_to_plot_thth):
    return varial.tools.ToolChainParallel('HistoLoader',
        list(varial.tools.HistoLoader(
            pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
            filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
                'Region_Comb' not in w.in_file_path and\
                any(w.in_file_path.endswith(f) for f in plot_hists),
            hook_loaded_histos=plot.loader_hook_merge_regions,
            name='HistoLoader_'+g,
            lookup_aliases=False,
            raise_on_empty_result=False,
            quiet_mode=True
            ) for g in samples))

def mk_histograms_merge(uncerts=uncerts, name='Histograms', samples=samples_to_plot_thth):
    return plot.mk_toolchain(name, samples,
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
            hook_loaded_histos=plot.loader_hook_merge_lep_channels,
            mod_log=common_plot.mod_log_usr(mod_dict),
            canvas_post_build_funcs=get_style()),
        pattern=None,
        input_result_path='../HistoLoader/HistoLoader*',
        # auto_legend=False,
        # name='HistogramsPostfit',
        # lookup_aliases=varial.settings.lookup_aliases
        )

def mk_histograms_merge_ratio_sb(uncerts=uncerts, name='HistogramsRatioSB'):
    return plot.mk_toolchain(name, samples_to_plot_thth,
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
            hook_loaded_histos=plot.loader_hook_merge_lep_channels,
            filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path,
            mod_log=common_plot.mod_log_usr(mod_dict),
            canvas_post_build_funcs=[
                common_plot.mod_pre_bot_hist(),
                common_plot.mk_bottom_plot_sig_bkg_ratio(),  # mk_pull_plot_func()
                # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                rnd.mk_legend_func(),
                common_plot.mod_post_canv(mod_dict),
                common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
            ]),
        pattern=None,
        input_result_path='../HistoLoader/HistoLoader*',
        # auto_legend=False,
        # name='HistogramsPostfit',
        # lookup_aliases=varial.settings.lookup_aliases
        )

def mk_histograms_no_sig(uncerts=uncerts, name='HistogramsNoSig', samples=samples_to_plot_thth):
    return plot.mk_toolchain(name, samples,
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
            filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-1200', 'TpTp_M-1600']) and w.sys_info == '',
            hook_loaded_histos=plot.loader_hook_merge_lep_channels,
            mod_log=common_plot.mod_log_usr(mod_dict),
            canvas_post_build_funcs= [
                common_plot.mod_pre_bot_hist(),
                common_plot.mk_split_err_ratio_plot_func_mod(),  # mk_pull_plot_func()
                # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                rnd.mk_legend_func(),
                common_plot.mod_post_canv(mod_dict),
                common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
            ]),
        pattern=None,
        input_result_path='../HistoLoader/HistoLoader*',
        # parallel=False
        # auto_legend=False,
        # name='HistogramsPostfit',
        # lookup_aliases=varial.settings.lookup_aliases
        )

def mk_histograms_sig_inj(name, excl_signal, samples=samples_to_plot_thth):
    return plot.mk_toolchain(name, samples,
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
            filter_keyfunc=lambda w: all(g not in w.sample for g in excl_signal) and w.sys_info == '',
            hook_loaded_histos=loader_hook_merge_sig_data,
            mod_log=common_plot.mod_log_usr(mod_dict),
            canvas_post_build_funcs= [
                common_plot.mod_pre_bot_hist(),
                common_plot.mk_split_err_ratio_plot_func_mod(),  # mk_pull_plot_func()
                # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                rnd.mk_legend_func(),
                common_plot.mod_post_canv(mod_dict),
                common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
            ]),
        pattern=None,
        input_result_path='../HistoLoader/HistoLoader*',
        # parallel=False
        # auto_legend=False,
        # name='HistogramsPostfit',
        # lookup_aliases=varial.settings.lookup_aliases
        )


def plot_merged_channels(final_dir):

    return varial.tools.ToolChain(final_dir, [
        mk_histoloader_merge(input_pattern),
        mk_histograms_merge(uncerts),
        mk_histograms_merge_ratio_sb(uncerts),
        mk_histograms_no_sig(uncerts),
        mk_histograms_sig_inj('HistogramsSigInj800', ['TpTp_M-1200', 'TpTp_M-1600']),
        mk_histograms_sig_inj('HistogramsSigInj1200', ['TpTp_M-0800', 'TpTp_M-1600']),
        mk_histograms_sig_inj('HistogramsSigInj1600', ['TpTp_M-0800', 'TpTp_M-1200']),
        # plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
        #     plotter_factory=plot.plotter_factory_uncerts(
        #         hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w), 
        #             analysis.rate_uncertainties, uncerts, include_rate=True)),
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # mk_toolchain('HistogramsNormToInt',
        #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=loader_hook_norm_to_int,
        #         plot_setup=stack_setup_norm_all_to_intgr)),
        # plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
        #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
        #         hook_loaded_histos=plot.loader_hook_compare_finalstates,
        #         mod_log=common_plot.mod_log_usr(mod_dict),
        #         canvas_post_build_funcs=get_style()
        #         ),
        #     parallel=True
        #     # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
        #     ),
        # mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
        #         hook_loaded_histos=loader_hook_compare_finalstates,
        #         )
        #     ),
        varial.tools.WebCreator()
        ])

def mk_sig_inj_test(final_dir):

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChain('TT_test', [
            mk_histoloader_merge(input_pattern_tt, samples=samples_to_plot_tt),
            mk_histograms_merge(uncerts, 'HistogramsBW', samples=samples_to_plot_bwbw),
            mk_histograms_merge(uncerts, 'HistogramsTH', samples=samples_to_plot_thth),
            # mk_histograms_merge_ratio_sb(uncerts),
            mk_histograms_no_sig(uncerts, samples=samples_to_plot_tt),
            mk_histograms_sig_inj('HistogramsSigInjBW800', ['TpTp_M-1200', 'TpTp_M-1600'], samples=samples_to_plot_bwbw),
            mk_histograms_sig_inj('HistogramsSigInjBW1200', ['TpTp_M-0800', 'TpTp_M-1600'], samples=samples_to_plot_bwbw),
            mk_histograms_sig_inj('HistogramsSigInjBW1600', ['TpTp_M-0800', 'TpTp_M-1200'], samples=samples_to_plot_bwbw),
            mk_histograms_sig_inj('HistogramsSigInjTH800', ['TpTp_M-1200', 'TpTp_M-1600'], samples=samples_to_plot_thth),
            mk_histograms_sig_inj('HistogramsSigInjTH1200', ['TpTp_M-0800', 'TpTp_M-1600'], samples=samples_to_plot_thth),
            mk_histograms_sig_inj('HistogramsSigInjTH1600', ['TpTp_M-0800', 'TpTp_M-1200'], samples=samples_to_plot_thth),
        ]),
        varial.tools.ToolChain('BB_test', [
            mk_histoloader_merge(input_pattern_bb, samples=samples_to_plot_bb),
            mk_histograms_merge(uncerts, 'HistogramsBW', samples=samples_to_plot_bb),
            mk_histograms_no_sig(uncerts, samples=samples_to_plot_bb),
            mk_histograms_sig_inj('HistogramsSigInjTW800', ['BpBp_M-1200', 'BpBp_M-1600'], samples=samples_to_plot_bb),
            mk_histograms_sig_inj('HistogramsSigInjTW1200', ['BpBp_M-0800', 'BpBp_M-1600'], samples=samples_to_plot_bb),
            mk_histograms_sig_inj('HistogramsSigInjTW1600', ['BpBp_M-0800', 'BpBp_M-1200'], samples=samples_to_plot_bb)
        ]),


        varial.tools.WebCreator()
        ])

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    all_tools = varial.tools.ToolChainParallel(final_dir,
        [
            # plot_merged_channels('PrefitPlots'),
            mk_sig_inj_test('SigInjTest'),
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()