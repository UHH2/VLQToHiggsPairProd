#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy
import pprint
import cPickle

import varial.settings as settings
import varial.rendering as rnd
import varial.generators as gen
import varial.wrappers as wrappers
import varial.tools as tools
import varial.extensions.limits as limits
import varial.analysis
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.plotter import Plotter

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
# import tptp_sframe 
# import compare_crs
import analysis
import sensitivity
import common_sensitivity
import combination_limits
import model_vlqpair
import bkg_only_fit
import treeproject_tptp
import tex_content_new as tex_content
import sel_opt_study
from get_eff_count import CountTable, EffTable # EffNumTable,
from plot_thesis import *

from ROOT import TLatex, TH2
import ROOT

# PUT THE SETTINGS BELOW INTO ONE GENERAL "THESIS-SETTINGS" FILE?

# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26'

# uncerts = list(analysis.all_uncerts)# or get_sys_dir()
# uncerts.remove('sfmu_trg')
# uncerts.remove('sflep_trg')

# source_dir_htrew = base_path+'/FullTreeProject/HTReweighting/TreeProject/'

# nom_pattern_htrew = [source_dir_htrew+'/TreeProjectorBkg/{0}.root',
#                source_dir_htrew+'/TreeProjectorTT/{0}.root']
# nom_pattern_htrew_bb = [source_dir_htrew+'/TreeProjectorBkg/{0}.root',
#                source_dir_htrew+'/TreeProjectorBB/{0}.root']
# sys_pattern_htrew = list(source_dir_htrew+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg']) +\
#               list(source_dir_htrew+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg'])
# sys_pattern_htrew_bb = list(source_dir_htrew+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg']) +\
#               list(source_dir_htrew+'/SysTreeProjectorsBB*/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg'])
                                                                                                            
                                                                                                            
# LLLLLLLLLLL               iiii                            iiii           tttt                           
# L:::::::::L              i::::i                          i::::i       ttt:::t                           
# L:::::::::L               iiii                            iiii        t:::::t                           
# LL:::::::LL                                                           t:::::t                           
#   L:::::L               iiiiiii    mmmmmmm    mmmmmmm   iiiiiii ttttttt:::::ttttttt        ssssssssss   
#   L:::::L               i:::::i  mm:::::::m  m:::::::mm i:::::i t:::::::::::::::::t      ss::::::::::s  
#   L:::::L                i::::i m::::::::::mm::::::::::m i::::i t:::::::::::::::::t    ss:::::::::::::s 
#   L:::::L                i::::i m::::::::::::::::::::::m i::::i tttttt:::::::tttttt    s::::::ssss:::::s
#   L:::::L                i::::i m:::::mmm::::::mmm:::::m i::::i       t:::::t           s:::::s  ssssss 
#   L:::::L                i::::i m::::m   m::::m   m::::m i::::i       t:::::t             s::::::s      
#   L:::::L                i::::i m::::m   m::::m   m::::m i::::i       t:::::t                s::::::s   
#   L:::::L         LLLLLL i::::i m::::m   m::::m   m::::m i::::i       t:::::t    ttttttssssss   s:::::s 
# LL:::::::LLLLLLLLL:::::Li::::::im::::m   m::::m   m::::mi::::::i      t::::::tttt:::::ts:::::ssss::::::s
# L::::::::::::::::::::::Li::::::im::::m   m::::m   m::::mi::::::i      tt::::::::::::::ts::::::::::::::s 
# L::::::::::::::::::::::Li::::::im::::m   m::::m   m::::mi::::::i        tt:::::::::::tt s:::::::::::ss  
# LLLLLLLLLLLLLLLLLLLLLLLLiiiiiiiimmmmmm   mmmmmm   mmmmmmiiiiiiii          ttttttttttt    sssssssssss    
                                                                                                            
                                                                                                         

final_rate_uncerts = {
    'TTbar' : 1.086,
    'WJets' : 1.06,
    'DYJets' : 1.05,
    'SingleTop' : 1.16,
    'Diboson' : 1.15,
    'QCD' : 2.0,
}

theta_model_bkg = model_vlqpair.get_model_no_norm(dum_rate_uncerts)
theta_model_norm = model_vlqpair.get_model_with_norm(dum_rate_uncerts)

theta_model_final = model_vlqpair.get_model_no_norm(final_rate_uncerts)

x_axis_lim="m_{T} [GeV]"
y_axis_lim="Upper limit on #sigma(pp #rightarrow TT)[pb]"

def mk_bkg_fit_tc(final_dir, pattern, sys_pat, filter_func=lambda _: True, theta_model=theta_model_bkg):
    # def tmp():
    return tools.ToolChain(final_dir, [
    tools.HistoLoader(
        name='HistoLoader',
        pattern=pattern,
        filter_keyfunc=filter_func,
        hook_loaded_histos=lambda w: bkg_only_fit.loader_hook(w, brs=[])
    ),
    tools.HistoLoader(
        name='HistoLoaderSys',
        pattern=sys_pat+pattern,
        filter_keyfunc=filter_func,
        hook_loaded_histos=lambda w: bkg_only_fit.remove_nom_wrps(bkg_only_fit.loader_hook(w, brs=[]))
    ),
    limits.ThetaLimits(
        name='ThetaLimit',
        cat_key=lambda w: w.category,
        sys_key=lambda w: w.sys_info,
        # name= 'ThetaLimitsSplit'+str(ind),
        # asymptotic=False,
        # brs=brs,
        # model_func=lambda w: model_func(w, signal)
        model_func=theta_model,
        calc_limits=False
        # out_name=signal
        # do_postfit=False,
    ),
    limits.ThetaPostFitPlot(
        name='PostFit',
        input_path='../ThetaLimit'
    ),
    limits.CorrelationMatrix(
        input_path='../ThetaLimit',
        proc_name=''
        ),
    Plotter(
        name='CorrelationPlot',
        input_result_path='../CorrelationMatrix',
        plot_setup=sensitivity.plot_setup_corr_matrix('colz text'),
        # hook_loaded_histos=loader_hook_triangle,
        # save_name_func=lambda w: w.save_name,
        canvas_post_build_funcs=[
            # varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
            common_plot.mk_tobject_draw_func(TLatex(0.67, 0.89, "#scale[0.5]{2.6 fb^{-1} (13 TeV)}")),
            ],
        raise_on_no_histograms=False
        )
    ])

# def get_lims_comp_mass_split(grp):
#     val_tup_list = []
#     wrps = grp.wrps
#     for wrp in wrps:
#         theta_res_exp = cPickle.loads(wrp.res_exp)
#         # theta_res_obs = cPickle.loads(wrp.res_obs)
#         if not theta_res_exp:
#             continue
#         x = theta_res_exp.x
#         y_exp = theta_res_exp.y
#         # y_obs = theta_res_obs.y
#         sigma1_low = theta_res_exp.bands[1][0]
#         sigma2_low = theta_res_exp.bands[0][0]
#         sigma1_high = theta_res_exp.bands[1][1]
#         sigma2_high = theta_res_exp.bands[0][1]
#         if not (len(x)==1):
#             monitor.message('limits.get_lims_mass_split', 'WARNING Not exactly one mass point in limit wrapper! ' +\
#                 'Length of x/sigma1_low/sigma1_high/sigma2_low/sigma2_high: %s/%s/%s/%s/%s' % (str(len(x)), str(len(sigma1_low)), str(len(sigma1_high)), str(len(sigma2_low)), str(len(sigma2_high))))
#         val_tup_list.append((x[0], y_exp[0], sigma1_low[0], sigma2_low[0], sigma1_high[0], sigma2_high[0]))
#     val_tup_list = sorted(val_tup_list, key=lambda w: w[0])
#     x_list = list(w[0] for w in val_tup_list)
#     y_exp_list = list(w[1] for w in val_tup_list)
#     sigma1_band_low = list(w[2] for w in val_tup_list)
#     sigma2_band_low = list(w[3] for w in val_tup_list)
#     sigma1_band_high = list(w[4] for w in val_tup_list)
#     sigma2_band_high = list(w[5] for w in val_tup_list)
#     # sigma2_band_high = list(w[6] for w in val_tup_list)
#     return x_list, y_exp_list, None, sigma1_band_low, sigma1_band_high, sigma2_band_low, sigma2_band_high




def mk_limit_tc(final_dir, brs, pattern, sys_pat, non_s_samples, signals, merge_final_states, filter_func=lambda _: True, asymptotic=True, plot_obs=False):

    def filter_signal(signal):
        def tmp(wrp):
            return any(a in wrp.sample for a in non_s_samples) or signal in wrp.sample
        return tmp

    # sig_list_with_fs = reduce(lambda x, y: x+y, (list(g + f for f in final_states) for g in signals))
    all_samples = non_s_samples + signals
    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoaderNom',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), pattern),
                filter_keyfunc=filter_func,
                hook_loaded_histos=lambda w: bkg_only_fit.loader_hook(w, brs=brs, merge=merge_final_states),
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in all_samples)
            ),
        tools.ToolChainParallel('HistoLoaderSys',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), pattern+sys_pat),
                filter_keyfunc=filter_func,
                hook_loaded_histos=lambda w: bkg_only_fit.remove_nom_wrps(bkg_only_fit.loader_hook(w, brs=brs, merge=merge_final_states)),
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in all_samples)
            ),
        # tools.HistoLoader(
        #     name='HistoLoader',
        #     pattern=pattern,
        #     filter_keyfunc=filter_func,
        #     hook_loaded_histos=lambda w: bkg_only_fit.loader_hook(w, brs=brs)
        # ),
        # tools.HistoLoader(
        #     name='HistoLoaderSys',
        #     pattern=sys_pat+pattern,
        #     filter_keyfunc=filter_func,
        #     hook_loaded_histos=lambda w: bkg_only_fit.remove_nom_wrps(bkg_only_fit.loader_hook(w, brs=brs))
        # ),
        tools.ToolChainParallel('ThetaLimits', list(
                limits.ThetaLimits(
                    name=sig,
                    input_path='../../HistoLoaderNom/HistoLoader*',
                    input_path_sys='../../HistoLoaderSys/HistoLoader*',
                    cat_key=lambda w: w.category,
                    sys_key=lambda w: w.sys_info,
                    filter_keyfunc=filter_signal(sig),
                    # name= 'ThetaLimitsSplit'+str(ind),
                    asymptotic=asymptotic,
                    # brs=brs,
                    # model_func=lambda w: model_func(w, signal)
                    model_func=lambda w: theta_model_final(w, sig.split('_')[0]+'*'),
                    hook_result_wrp=sel_opt_study.hook_lim_graph_comp(final_dir)
                    # out_name=signal
                    # do_postfit=False,
                ) for sig in signals
            )
        ),
        limits.LimitGraphsNew(
            limit_path='../ThetaLimits/*/ThetaHistos*.root',
            plot_obs=plot_obs,
            split_mass=True,
            plot_1sigmabands=True,
            plot_2sigmabands=True,
            axis_labels=(x_axis_lim, y_axis_lim),
            # get_lim_params=get_lims_comp_mass_split,
            ),
        Plotter(
            name='LimitCurvesCompared',
            input_result_path='../LimitGraphsNew',
            # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
            # plot_setup=plot_setup,
            hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs),
            plot_grouper=lambda ws: varial.gen.group(
                    ws, key_func=lambda w: w.save_name),
            # save_name_func=varial.plotter.save_by_name_with_hash
            save_name_func=lambda w: w.save_name,
            plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                th_x=common_sensitivity.theory_masses,
                th_y=common_sensitivity.theory_cs),
            keep_content_as_result=True,
            # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
            canvas_post_build_funcs=[
                rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                # common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                ],
            # save_lin_log_scale=True
            ),
        ])

def mk_tc_limgraphs_exp_lim(final_dir, lim_path):
    return tools.ToolChain(final_dir, [
        limits.LimitGraphsNew(
            limit_path=lim_path,
            plot_obs=False,
            split_mass=False,
            plot_1sigmabands=False,
            plot_2sigmabands=False,
            hook_loaded_graphs=sel_opt_study.loader_hook_lim_graphs_comp,
            group_graphs=lambda ws: varial.gen.group(
                    ws, key_func=lambda w: w.selection),
            axis_labels=(x_axis_lim, y_axis_lim),
            setup_graphs=sel_opt_study.setup_graphs,
            get_lim_params=sel_opt_study.get_lims_comp_mass_split,
            ),
        Plotter(
            name='LimitCurvesCompared',
            input_result_path='../LimitGraphsNew',
            # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
            # plot_setup=plot_setup,
            # hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs),
            hook_loaded_histos=sel_opt_study.hook_graph_def,
            plot_grouper=lambda ws: varial.gen.group(
                    ws, key_func=lambda w: w.save_name),
            # save_name_func=varial.plotter.save_by_name_with_hash
            save_name_func=lambda w: w.save_name,
            # plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
            #     th_x=common_sensitivity.theory_masses,
            #     th_y=common_sensitivity.theory_cs),
            plot_setup=sel_opt_study.setup_graphs_plot,
            # keep_content_as_result=True,
            # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
            # canvas_post_build_funcs=[
            #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
            #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
            #     # common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
            #     ],
            # save_lin_log_scale=True
            ),
        ])

def mk_triangle(lim_path):
    return varial.tools.ToolChain('LimitTriangle',[
        vlq_common.TriangleMassLimitPlots(
            limit_rel_path=lim_path,
            leg_x='BR(T #rightarrow tH)', leg_y='BR(T #rightarrow bW)'
            ),
        varial.plotter.Plotter(
            name='PlotterBoxExp',
            input_result_path='../TriangleMassLimitPlots',
            filter_keyfunc=lambda w: 'exp' in w.save_name,
            plot_setup=sensitivity.plot_setup_triangle('col'),
            save_name_func=lambda w: w.save_name,
            canvas_post_build_funcs=[sensitivity.DrawLess700(),
                # common_plot.mk_tobject_draw_func(TLatex(0.75, 0.79, "#scale[0.7]{#bf{CMS}}")),
                # common_plot.mk_tobject_draw_func(TLatex(0.67, 0.73, "#scale[0.6]{#it{Simulation}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}")),]
            ),

        varial.plotter.Plotter(
            name='PlotterBoxObs',
            input_result_path='../TriangleMassLimitPlots',
            filter_keyfunc=lambda w: 'obs' in w.save_name,
            plot_setup=sensitivity.plot_setup_triangle('col'),
            save_name_func=lambda w: w.save_name,
            canvas_post_build_funcs=[sensitivity.DrawLess700(),
                # common_plot.mk_tobject_draw_func(TLatex(0.75, 0.79, "#scale[0.7]{#bf{CMS}}")),
                # common_plot.mk_tobject_draw_func(TLatex(0.66, 0.73, "#scale[0.6]{#it{Preliminary}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}")),]
            ),
        ])

def unselect_standard_th_uncerts(wrp):
    sample = os.path.basename(wrp.file_path)
    sample = os.path.splitext(sample)[0]
    sample = sample.split('-')[-1]
    if any(s == sample for s in ['Diboson', 'QCD']):
        if any(g in wrp.file_path for g in ['ScaleVar', 'PDF']):
            return False
    if 'PSScale' in wrp.file_path and not sample == analysis.ttbar_smpl:
        return False
    return True

final_regions = [
    'SignalRegion2b_Mu45',
    'SignalRegion1b_Mu45',
    'SidebandRegion_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion1b_El45',
    'SidebandRegion_El45',
]

sb_regions = [
    'SidebandTTJetsRegion_El45',
    'SidebandTTJetsRegion_Mu45',
    'SidebandWPlusJetsRegion_El45',
    'SidebandWPlusJetsRegion_Mu45',
]

brs_th_only = { 'w' : 0.0, 'z' : 0.0, 'h' : 1.0 }
all_brs = [
    ('bW0p5_tZ0p25_tH0p25', { 'w' : 0.5, 'h' : 0.25, 'z' : 0.25 }),
    ('bW0p0_tZ0p5_tH0p5', { 'w' : 0.0, 'z' : 0.5, 'h' : 0.5 }),
    ('bW0p0_tZ0p0_tH1p0', { 'w' : 0.0, 'z' : 0.0, 'h' : 1.0 }),
    ('bW1p0_tZ0p0_tH0p0', { 'w' : 1.0, 'z' : 0.0, 'h' : 0.0 }),
    ('bW0p0_tZ0p2_tH0p8', { 'w' : 0.0, 'z' : 0.2, 'h' : 0.8 }),
    ('bW0p0_tZ0p4_tH0p6', { 'w' : 0.0, 'z' : 0.4, 'h' : 0.6 }),
    ('bW0p0_tZ0p6_tH0p4', { 'w' : 0.0, 'z' : 0.6, 'h' : 0.4 }),
    ('bW0p0_tZ0p8_tH0p2', { 'w' : 0.0, 'z' : 0.8, 'h' : 0.2 }),
    ('bW0p0_tZ1p0_tH0p0', { 'w' : 0.0, 'z' : 1.0, 'h' : 0.0 }),
    ('bW0p2_tZ0p0_tH0p8', { 'w' : 0.2, 'z' : 0.0, 'h' : 0.8 }),
    ('bW0p2_tZ0p2_tH0p6', { 'w' : 0.2, 'z' : 0.2, 'h' : 0.6 }),
    ('bW0p2_tZ0p4_tH0p4', { 'w' : 0.2, 'z' : 0.4, 'h' : 0.4 }),
    ('bW0p2_tZ0p6_tH0p2', { 'w' : 0.2, 'z' : 0.6, 'h' : 0.2 }),
    ('bW0p2_tZ0p8_tH0p0', { 'w' : 0.2, 'z' : 0.8, 'h' : 0.0 }),
    ('bW0p4_tZ0p0_tH0p6', { 'w' : 0.4, 'z' : 0.0, 'h' : 0.6 }),
    ('bW0p4_tZ0p2_tH0p4', { 'w' : 0.4, 'z' : 0.2, 'h' : 0.4 }),
    ('bW0p4_tZ0p4_tH0p2', { 'w' : 0.4, 'z' : 0.4, 'h' : 0.2 }),
    ('bW0p4_tZ0p6_tH0p0', { 'w' : 0.4, 'z' : 0.6, 'h' : 0.0 }),
    ('bW0p6_tZ0p0_tH0p4', { 'w' : 0.6, 'z' : 0.0, 'h' : 0.4 }),
    ('bW0p6_tZ0p2_tH0p2', { 'w' : 0.6, 'z' : 0.2, 'h' : 0.2 }),
    ('bW0p6_tZ0p4_tH0p0', { 'w' : 0.6, 'z' : 0.4, 'h' : 0.0 }),
    ('bW0p8_tZ0p0_tH0p2', { 'w' : 0.8, 'z' : 0.0, 'h' : 0.2 }),
    ('bW0p8_tZ0p2_tH0p0', { 'w' : 0.8, 'z' : 0.2, 'h' : 0.0 }),
    ]

all_brs_bb = combination_limits.br_list_bb

filter_func_bkg_norew = lambda w: unselect_standard_th_uncerts(w) and any(a in os.path.basename(w.file_path) for a in non_sig_samples) and sensitivity.default_selection(w) and any(w.in_file_path.split('/')[0] == a for a in sb_regions)
filter_func_bkg_htrew = lambda w: filter_func_bkg_norew(w) and common_plot.unselect_theory_uncert(w)

filter_func_exp_lim_norew = lambda w: unselect_standard_th_uncerts(w) and sensitivity.default_selection(w) and any(w.in_file_path.split('/')[0] == a for a in final_regions) and 'Run2015CD' not in os.path.basename(w.file_path)
filter_func_exp_lim_htrew = lambda w: filter_func_exp_lim_norew(w) and common_plot.unselect_theory_uncert(w)

filter_func_obs_lim_htrew = lambda w: common_plot.unselect_theory_uncert(w) and sensitivity.default_selection(w) and any(w.in_file_path.split('/')[0] == a for a in final_regions)

def mk_tc_comp_bkg_mdl(final_dir):
    return tools.ToolChainParallel(final_dir, [
            mk_bkg_fit_tc('BkgOnlyNoReweighting', nom_pattern_norew, sys_pattern_norew, filter_func_bkg_norew),
            mk_bkg_fit_tc('BkgOnlyHTReweighting', nom_pattern_htrew, sys_pattern_htrew, filter_func_bkg_htrew),
            mk_limit_tc('ExpLimitNoReweighting', brs_th_only, nom_pattern_norew, sys_pattern_norew, bkg_samples, list(a + '_thth' for a in treeproject_tptp.tptp_signals), merge_final_states=False, filter_func=filter_func_exp_lim_norew, asymptotic=False),
            mk_limit_tc('ExpLimitHTReweighting', brs_th_only, nom_pattern_htrew, sys_pattern_htrew, bkg_samples, list(a + '_thth' for a in treeproject_tptp.tptp_signals), merge_final_states=False, filter_func=filter_func_exp_lim_htrew, asymptotic=False),
            mk_tc_limgraphs_exp_lim('CompExpLimits', '../../ExpLimit*/ThetaLimits/*'),
            mk_bkg_fit_tc('NormEvalHTReweighting', nom_pattern_htrew, sys_pattern_htrew, filter_func_bkg_htrew, theta_model=theta_model_norm),
            tools.WebCreator()
        ], n_workers=1)


def mk_tc_all_limits(final_dir):
    return tools.ToolChain(final_dir, [
            tools.ToolChainParallel('IndLimits', list(
                    mk_limit_tc('Limit_'+n, brs, nom_pattern_htrew, sys_pattern_htrew, non_sig_samples, treeproject_tptp.tptp_signals, merge_final_states=True, filter_func=filter_func_obs_lim_htrew, asymptotic=False, plot_obs=True)
                    for n, brs in all_brs
                ), n_workers=1),
            mk_triangle(list('../../IndLimits/Limit_%s/LimitCurvesCompared' % i[0]
                for i in all_brs if i[0] not in ['bW0p5_tZ0p25_tH0p25', 'bW0p0_tZ0p5_tH0p5'])),
            tools.WebCreator()
            ]
        )


def mk_tc_all_limits_bb(final_dir):
    return tools.ToolChain(final_dir, [
            tools.ToolChainParallel('IndLimits', list(
                    mk_limit_tc('Limit_'+n, brs, nom_pattern_htrew_bb, sys_pattern_htrew_bb, non_sig_samples, treeproject_tptp.bpbp_signals, merge_final_states=True, filter_func=filter_func_obs_lim_htrew, asymptotic=False, plot_obs=True)
                    for n, brs in all_brs_bb
                ), n_workers=1),
            mk_triangle(list('../../IndLimits/Limit_%s/LimitCurvesCompared' % i[0]
                for i in all_brs_bb if i[0] not in ['tW0p5_bZ0p25_bH0p25', 'tW0p0_bZ0p5_bH0p5'])),
            tools.WebCreator()
            ]
        )




                                                                   
                                                                   
# TTTTTTTTTTTTTTTTTTTTTTT                                        
# T:::::::::::::::::::::T                                        
# T:::::::::::::::::::::T                                        
# T:::::TT:::::::TT:::::T                                        
# TTTTTT  T:::::T  TTTTTT    eeeeeeeeeeee    xxxxxxx      xxxxxxx
#         T:::::T          ee::::::::::::ee   x:::::x    x:::::x 
#         T:::::T         e::::::eeeee:::::ee  x:::::x  x:::::x  
#         T:::::T        e::::::e     e:::::e   x:::::xx:::::x   
#         T:::::T        e:::::::eeeee::::::e    x::::::::::x    
#         T:::::T        e:::::::::::::::::e      x::::::::x     
#         T:::::T        e::::::eeeeeeeeeee       x::::::::x     
#         T:::::T        e:::::::e               x::::::::::x    
#       TT:::::::TT      e::::::::e             x:::::xx:::::x   
#       T:::::::::T       e::::::::eeeeeeee    x:::::x  x:::::x  
#       T:::::::::T        ee:::::::::::::e   x:::::x    x:::::x 
#       TTTTTTTTTTT          eeeeeeeeeeeeee  xxxxxxx      xxxxxxx
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   


def mk_tc_tex(source_dir):
    tc_tex = [
        tex_content.mk_plot_ind(
            (
                ('pt_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('pt_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('mass_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('mass_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_lin.pdf'),
            ), name='HiggsPlotsNoDat'
        ),
        tex_content.mk_plot_ind(
            (
                ('ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/ST_lin.pdf'),
                # ('HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/HT_lin.pdf'),
                ('n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_ak4_lin.pdf'),
                ('n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_ak8_lin.pdf'),
                # ('nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                # ('nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                # ('noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                # ('noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                # ('nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/primary_lepton_pt_lin.pdf'),
                ('pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/pt_ld_ak4_jet_lin.pdf'),
                ('pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/pt_subld_ak4_jet_lin.pdf'),
                ('topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/topjets[0].m_pt_lin.pdf'),
                ('topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/topjets[1].m_pt_lin.pdf'),
                ('met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/met_lin.pdf'),
                # ('jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/jets[].m_pt_lin.pdf'),
                ('n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_additional_btags_medium_log.pdf'),
                ('n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_higgs_tags_1b_med_log.pdf'),
                ('n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_higgs_tags_2b_med_log.pdf'),
                # ('n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/n_prim_vertices_lin.pdf'),
            ), name='PreselectionPlotsNoDat'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_tt_HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_tt_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak4_lin.pdf'),
                ('sb_tt_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak8_lin.pdf'),
                ('sb_tt_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_tt_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_tt_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_tt_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_tt_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_tt_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_tt_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_tt_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_tt_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_tt_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_tt_met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/met_lin.pdf'),
                ('sb_tt_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_tt_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_tt_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_tt_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_tt_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_prim_vertices_lin.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_wjets_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak4_lin.pdf'),
                ('sb_wjets_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak8_lin.pdf'),
                ('sb_wjets_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_wjets_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_wjets_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_wjets_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_wjets_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_wjets_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_wjets_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_wjets_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_wjets_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_wjets_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_wjets_met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/met_lin.pdf'),
                ('sb_wjets_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_wjets_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_wjets_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_wjets_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_wjets_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_prim_vertices_lin.pdf'),
            ), name='SidebandPlotsSyst'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_ttbar_all', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntAll/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_ttbar_exp', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntExpSyst/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_ttbar_theo', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntThSyst/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_lin.pdf'),
                ('sb_wjets_all', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntAll/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_exp', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntExpSyst/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_theo', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntThSyst/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_lin.pdf'),
            ), name='NormPlotsSideband'
        ),
        tex_content.mk_plot_ind(
            (
                ('top_pt_reweight_sb', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('top_pt_reweight_norm', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/HistogramsNormToIntAll/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('top_pt_reweight_comp_unc', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/HistogramsCompUncerts/StackedAll/SidebandTTJetsRegion/ST_rebin_flex__TTbar__top_pt_reweight_log.pdf'),
            ), name='TopPtPlots'
        ),
        tex_content.mk_plot_ind(
            (
                ('lin_func_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('lin_func_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysFit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
            ), name='FitPlots'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_tt_HT', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_tt_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak4_lin.pdf'),
                ('sb_tt_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak8_lin.pdf'),
                ('sb_tt_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_tt_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_tt_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_tt_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_tt_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_tt_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_tt_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_tt_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_tt_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_tt_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_tt_met', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/met_lin.pdf'),
                ('sb_tt_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_tt_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_tt_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_tt_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_tt_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_prim_vertices_lin.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_HT', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_wjets_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak4_lin.pdf'),
                ('sb_wjets_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak8_lin.pdf'),
                ('sb_wjets_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_wjets_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_wjets_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_wjets_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_wjets_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_wjets_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_wjets_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_wjets_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_wjets_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_wjets_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_wjets_met', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/met_lin.pdf'),
                ('sb_wjets_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_wjets_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_wjets_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_wjets_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_wjets_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_prim_vertices_lin.pdf'),
            ), name='SidebandPlotsSystWithRew'
        ),
        tex_content.mk_plot_ind(
            (
                ('comp_htrew_theo_uncerts_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompScaleVarHTRew/StackedAll/BaseLineSelection/ST_rebin_flex__TTbar__comp_th_log.pdf'),
                ('comp_htrew_theo_uncerts_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompScaleVarHTRew/StackedAll/BaseLineSelection/ST_rebin_flex__WJets__comp_th_log.pdf'),
                ('comp_norew_jec_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__jec_log.pdf'),
                ('comp_norew_jec_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__jec_log.pdf'),
                ('comp_norew_jec_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__jec_log.pdf'),
                ('comp_norew_jer_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__jer_log.pdf'),
                ('comp_norew_jer_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__jer_log.pdf'),
                ('comp_norew_jer_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__jer_log.pdf'),
                ('comp_norew_btag_bc_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__btag_bc_log.pdf'),
                ('comp_norew_btag_bc_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__btag_bc_log.pdf'),
                ('comp_norew_btag_bc_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__btag_bc_log.pdf'),
                ('comp_norew_btag_udsg_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__btag_udsg_log.pdf'),
                ('comp_norew_btag_udsg_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__btag_udsg_log.pdf'),
                ('comp_norew_btag_udsg_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__btag_udsg_log.pdf'),
                ('comp_norew_scalevar_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__ScaleVar_log.pdf'),
                ('comp_norew_scalevar_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__ScaleVar_log.pdf'),
                ('comp_norew_scalevar_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__ScaleVar_log.pdf'),
                ('comp_norew_pdf_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__PDF_log.pdf'),
                ('comp_norew_pdf_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__PDF_log.pdf'),
                ('comp_norew_pdf_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200__PDF_log.pdf'),
            ), name='CompSystUncerts'
        ),
        tex_content.mk_plot_ind(
            (
                ('bkg_only_check_norew_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyNoReweighting/PostFit/cnv_post_fit_.pdf'),
                ('bkg_only_check_htrew_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyHTReweighting/PostFit/cnv_post_fit_.pdf'),
                ('bkg_only_check_norew_corr_mat', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyNoReweighting/CorrelationPlot/correlation_matrix_d42c0f_lin.pdf'),
                ('bkg_only_check_htrew_corr_mat', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyHTReweighting/CorrelationPlot/correlation_matrix_d42c0f_lin.pdf'),
            ), name='CompBkgModels'
        ),
        tex_content.mk_plot_ind(
            (
                ('norm_eval_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/NormEvalHTReweighting/PostFit/cnv_post_fit_.pdf'),
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('0h_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='PostFitPlots'
        ),
        tex_content.mk_plot_ind(
            (
                # ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                # ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('0h_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('sb_tt_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('0h_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='PreFitPlots'
        ),
        tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir, 'FinalLimitsTT/IndLimits/Limit_bW0p0_tZ0p0_tH1p0/ThetaLimits/{0}'), 'SysTabs', mass_points=['TpTp_M-0800', 'TpTp_M-1200', 'TpTp_M-1600'], regions=final_regions),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSAll/count_table_content.tex', name='EffTableCompFSAll'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSFinalCuts/count_table_content.tex', name='EffTableCompFSFinalCuts'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSFinalCutsComb/count_table_content.tex', name='EffTableCompFSFinalCutsComb'),
        # tex_content.mk_autoTable(path_an+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePostFit/count_table_content.tex', name='CountTablePostFit'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePreFit/count_table_content.tex', name='CountTablePreFit'),
    ]
    tc_tex = tools.ToolChain('CopyPlots', [
        tools.ToolChain('TexThesis', tc_tex),
        tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
        ])
    return tc_tex

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    all_tools = tools.ToolChainParallel(final_dir,
        [
            mk_tc_all_limits('FinalLimitsTT'),
            mk_tc_all_limits_bb('FinalLimitsBB'),
            mk_tc_tex(final_dir),
            tools.WebCreator()
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    tools.Runner(all_tools, default_reuse=True)
    # tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()