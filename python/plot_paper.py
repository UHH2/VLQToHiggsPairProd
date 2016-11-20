#!/usr/bin/env python

import sys
import os
import time

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

bkgs_to_plot = [
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015CD',
    # 'Diboson'
    'TTbar_split'
]

samples_to_plot = bkgs_to_plot + list(g + '_thth' for g in plot.less_signals)

samples_to_plot_higgs = bkgs_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in plot.final_states_to_plot) for g in plot.less_signals))

samples_for_tables = bkgs_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in plot.final_states_to_plot) for g in plot.almost_all_signals))

base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24'

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
            'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },

    'nomass_boost_2b_mass_softdrop_rebin_flex' : {
            'y_max_fct' : 1.3,
            'title' : 'M_{jet} [GeV]',
            'bin_width' : 5,
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.4,
            'set_leg_1_col_lin' : {
                    'x_pos': 0.74,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    'nobtag_boost_mass_nsjbtags' : {
            'title' : 'N(subjet b-tags)',
            'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            'set_leg_1_col_log' : {
                    'x_pos': 0.74,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'text_box_log' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    }

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

source_dir = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
    'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
    'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/TreeProject'
uncerts = analysis.all_uncerts + ['sfel_trg'] # or get_sys_dir()
nom_pattern = [source_dir+'/TreeProjector/{0}.root',
               source_dir+'/TreeProjectorDiboson/{0}.root']
sys_pattern = list(source_dir+'/SysTreeProjectors/%s*/{0}.root'% i for i in uncerts) +\
              list(source_dir+'/SysTreeProjectorsDiboson/%s*/{0}.root'% i for i in uncerts)
input_pattern = nom_pattern+sys_pattern

theta_lim_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
    'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
    'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/Limit/'\
    'BackgroundOnlyFitNoTheory/CR/ThetaLimit/'


def plot_merged_channels_higgs(final_dir):
    # plot_hists = ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
    #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']
    plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt', 'nobtag_boost_mass_nsjbtags']

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoader',
        list(varial.tools.HistoLoader(
            pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
            filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot_higgs) and\
                'Region_Comb' not in w.in_file_path and\
                any(w.in_file_path.endswith(f) for f in plot_hists) and\
                common_plot.unselect_theory_uncert(w),
            hook_loaded_histos=plot.loader_hook_merge_regions,
            name='HistoLoader_'+g,
            lookup_aliases=False,
            raise_on_empty_result=False,
            quiet_mode=True
            ) for g in samples_to_plot_higgs)),
        plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot,
            filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
            plotter_factory=plot.plotter_factory_uncerts(
                hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w), 
                    analysis.rate_uncertainties, uncerts, include_rate=True)),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # mk_toolchain('HistogramsNormToInt',
        #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=loader_hook_norm_to_int,
        #         plot_setup=stack_setup_norm_all_to_intgr)),
        plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
                hook_loaded_histos=plot.loader_hook_compare_finalstates,
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            parallel=True
            # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
            ),
        # mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
        #         hook_loaded_histos=loader_hook_compare_finalstates,
        #         )
        #     ),
        varial.tools.WebCreator()
        ])


def plot_merged_channels_postfit(final_dir):
    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoaderPost',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_to_plot) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=plot.loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot)),
        plot.mk_toolchain('HistogramsPostfit', samples_to_plot,
            plotter_factory=sensitivity.plotter_factory_postfit(theta_lim_path, '', analysis.rate_uncertainties, uncerts, True,
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        # plot.mk_toolchain('HistogramsPostfitCompareUncerts', samples_to_plot,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in ['TTbar_split', 'WJets', 'DYJets', 'TpTp_M-0800', 'TpTp_M-1600']) and\
        #         any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),
        #     plotter_factory=plot.plotter_factory_uncerts(rate_uncertainties, sys_uncerts,
        #         hook_loaded_histos=lambda w: loader_hook_split_uncert(w, theta_lim_path, signal, rate_uncertainties, sys_uncerts, include_rate),
        #     ),
        #     pattern=None, input_result_path='../HistoLoaderPost/HistoLoader*'
        #     ),
        # plot.mk_toolchain('HistogramsTables', samples_for_tables,
        #     plotter_factory=plotter_factory_postfit(theta_lim_path, signal, rate_uncertainties, sys_uncerts, include_rate),
        #     pattern=None,
        #     input_result_path='../HistoLoaderPost/HistoLoader*',
        #     # auto_legend=False,
        #     # name='HistogramsPostfit',
        #     # lookup_aliases=varial.settings.lookup_aliases
        #     ),
        # CountTable([
        #         common_plot.table_block_signal,
        #         common_plot.table_block_background,
        #         [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
        #         [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
        #     ],
        #     common_plot.get_table_category_block('HistogramsTables'),
        #     name='CountTablePostFit'
        #     ),
        # CountTable([
        #         common_plot.table_block_signal_small,
        #         common_plot.table_block_background,
        #         [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
        #         [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
        #     ],
        #     common_plot.get_table_category_block('HistogramsTables', style='PAS'),
        #     squash_errs=True,
        #     name='CountTablePostFitPAS'
        #     ),
        varial.tools.WebCreator()
        ])

def plot_merged_channels_tables(final_dir):
    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoaderPost',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_for_tables) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=plot.loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_for_tables)),
        plot.mk_toolchain('HistogramsTables', samples_for_tables,
            plotter_factory=sensitivity.plotter_factory_postfit(theta_lim_path, '', analysis.rate_uncertainties, uncerts, True),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsTablesPrefit', samples_for_tables,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        CountTable([
                common_plot.table_block_signal_small,
                common_plot.table_block_background_no_dib,
                [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
            ],
            common_plot.get_table_category_block('HistogramsTables', style='paper'),
            squash_errs=True,
            name='CountTablePostFit'
            ),
        CountTable([
                common_plot.table_block_signal_small,
                common_plot.table_block_background_no_dib,
                [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
            ],
            common_plot.get_table_category_block('HistogramsTablesPrefit', style='paper'),
            squash_errs=True,
            name='CountTablePreFit'
            ),
        EffTable([
                common_plot.table_block_signal_fs_800,
                common_plot.table_block_signal_fs_1600,
            ],
            common_plot.get_table_category_block('HistogramsTables', style='paper'),
            common_plot.norm_factors,
            squash_errs=True,
            name='EffTableCompFS'
            ),
        varial.tools.WebCreator()
        ])

def mk_tc_tex(source_dir):
    tc_tex_an = [
        tex_content.mk_plot_ind(
            (
                ('higgs_tag_mass', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_rebin_flex_lin.pdf'),
                ('higgs_tag_sjbtags', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_log.pdf'),
                ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_h1b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('st_h2b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='PaperPlots'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS'),
        # tex_content.mk_autoTable(path_an+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePostFit/count_table_content.tex', name='CountTablePostFit'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePreFit/count_table_content.tex', name='CountTablePreFit'),
        # tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/ThetaLimits', 'SysTabs', mass_points=['TTM0700', 'TTM1200', 'TTM1700'], regions=regions),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/EffTableCompFSPAS/count_table_content.tex', name='EffTableCompFS_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/BackgroundOnlyFitNoTheory/CR/PostFitPlots/CountTablePostFitPAS/count_table_content.tex', name='CountTablePostFit_'+name),
        
    ]
    tc_tex_an = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexPaper', tc_tex_an),
        varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:PAS-Dir/notes/B2G-16-024/trunk/', src='../TexPaper/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True),
        ])
    return tc_tex_an

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    all_tools = varial.tools.ToolChainParallel(final_dir,
        [
            plot_merged_channels_higgs('HiggsPlots'),
            plot_merged_channels_postfit('PostFitPlots'),
            plot_merged_channels_tables('Tables'),
            mk_tc_tex(final_dir)
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()