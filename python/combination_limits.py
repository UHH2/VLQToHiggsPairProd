#!/usr/bin/env python

# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as vlq_common
import varial.tools
import os
import glob
import sys


import common_plot_new as common_plot
import plot_new as plot
from varial.extensions import git, limits
import varial.generators as gen
import varial.rendering as rnd

from varial.extensions.limits import ThetaLimits, ThetaPostFitPlot, CorrelationMatrix

from ROOT import TLatex

varial.settings.max_num_processes = 24
varial.settings.max_open_root_files = 1500

import sensitivity
import analysis
# import treeproject_tptp
import model_vlqpair
import theta_combined_template
import common_sensitivity
import tex_content_new as tex_content
from get_eff_count import CountTable, EffTable # EffNumTable,

import UHH2.VLQSemiLepPreSel.common as vlq_common


# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24'
# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'
base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26'

base_path_julie = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2'\
    '/VLQToHiggsPairProd/NewSamples-76X-v1/Julie_files/templates_minMlb_'

file_suffix = '_2p318fb_rebinnedDV.root'

# pattern_tt = [base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/TreeProjector/*.root',
#     base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/TreeProjectorDiboson/*.root']
pattern_tt = [base_path+'/FullTreeProject/HTReweighting/TreeProject/TreeProjectorBkg/*.root',
    base_path+'/FullTreeProject/HTReweighting/TreeProject/TreeProjectorTT/*.root']

# pattern_bb = [base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/TreeProjector/*.root',base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/TreeProjectorBB/*.root',
#     base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/TreeProjectorDiboson/*.root']
pattern_bb = [base_path+'/FullTreeProject/HTReweighting/TreeProject/TreeProjectorBkg/*.root',
    base_path+'/FullTreeProject/HTReweighting/TreeProject/TreeProjectorBB/*.root']


# sys_path = base_path+'/Run8_withHighMassTTbarSample/'\
#     'RunAnalysis/HTReweighting/TreeProject/SysTreeProjectors'
sys_path = base_path+'/FullTreeProject/HTReweighting/TreeProject/SysTreeProjectors'

uncerts = analysis.all_uncerts

# sys_pat_tt = list(sys_path+'/%s*/*.root'% i for i in uncerts) + list(sys_path+'Diboson/%s*/*.root'% i for i in uncerts)
sys_pat_tt = list(sys_path+'Bkg/%s*/*.root'% i for i in uncerts) + list(sys_path+'TT*/%s*/*.root'% i for i in uncerts)

# sys_pat_bb = list(sys_path+'/%s*/*.root'% i for i in uncerts) + list(sys_path+'Diboson/%s*/*.root'% i for i in uncerts) + list(sys_path+'BB/%s*/*.root'% i for i in uncerts)
sys_pat_bb = list(sys_path+'Bkg/%s*/*.root'% i for i in uncerts) + list(sys_path+'BB*/%s*/*.root'% i for i in uncerts)

br_list_tt = [
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

br_list_bb = [
    ('tW0p5_bZ0p25_bH0p25', { 'w' : 0.5, 'h' : 0.25, 'z' : 0.25 }),
    ('tW0p0_bZ0p5_bH0p5', { 'w' : 0.0, 'z' : 0.5, 'h' : 0.5 }),
    ('tW0p0_bZ0p0_bH1p0', { 'w' : 0.0, 'z' : 0.0, 'h' : 1.0 }),
    ('tW1p0_bZ0p0_bH0p0', { 'w' : 1.0, 'z' : 0.0, 'h' : 0.0 }),
    ('tW0p0_bZ0p2_bH0p8', { 'w' : 0.0, 'z' : 0.2, 'h' : 0.8 }),
    ('tW0p0_bZ0p4_bH0p6', { 'w' : 0.0, 'z' : 0.4, 'h' : 0.6 }),
    ('tW0p0_bZ0p6_bH0p4', { 'w' : 0.0, 'z' : 0.6, 'h' : 0.4 }),
    ('tW0p0_bZ0p8_bH0p2', { 'w' : 0.0, 'z' : 0.8, 'h' : 0.2 }),
    ('tW0p0_bZ1p0_bH0p0', { 'w' : 0.0, 'z' : 1.0, 'h' : 0.0 }),
    ('tW0p2_bZ0p0_bH0p8', { 'w' : 0.2, 'z' : 0.0, 'h' : 0.8 }),
    ('tW0p2_bZ0p2_bH0p6', { 'w' : 0.2, 'z' : 0.2, 'h' : 0.6 }),
    ('tW0p2_bZ0p4_bH0p4', { 'w' : 0.2, 'z' : 0.4, 'h' : 0.4 }),
    ('tW0p2_bZ0p6_bH0p2', { 'w' : 0.2, 'z' : 0.6, 'h' : 0.2 }),
    ('tW0p2_bZ0p8_bH0p0', { 'w' : 0.2, 'z' : 0.8, 'h' : 0.0 }),
    ('tW0p4_bZ0p0_bH0p6', { 'w' : 0.4, 'z' : 0.0, 'h' : 0.6 }),
    ('tW0p4_bZ0p2_bH0p4', { 'w' : 0.4, 'z' : 0.2, 'h' : 0.4 }),
    ('tW0p4_bZ0p4_bH0p2', { 'w' : 0.4, 'z' : 0.4, 'h' : 0.2 }),
    ('tW0p4_bZ0p6_bH0p0', { 'w' : 0.4, 'z' : 0.6, 'h' : 0.0 }),
    ('tW0p6_bZ0p0_bH0p4', { 'w' : 0.6, 'z' : 0.0, 'h' : 0.4 }),
    ('tW0p6_bZ0p2_bH0p2', { 'w' : 0.6, 'z' : 0.2, 'h' : 0.2 }),
    ('tW0p6_bZ0p4_bH0p0', { 'w' : 0.6, 'z' : 0.4, 'h' : 0.0 }),
    ('tW0p8_bZ0p0_bH0p2', { 'w' : 0.8, 'z' : 0.0, 'h' : 0.2 }),
    ('tW0p8_bZ0p2_bH0p0', { 'w' : 0.8, 'z' : 0.2, 'h' : 0.0 }),
    ]

regions = [
    'SignalRegion1b_El45',
    'SignalRegion1b_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion2b_Mu45',
    'minMlb_2p318fb_isE_nT0p_nW0_nB0',
    'minMlb_2p318fb_isE_nT0p_nW0_nB1',
    'minMlb_2p318fb_isE_nT0p_nW0_nB2',
    'minMlb_2p318fb_isE_nT0p_nW0_nB3p',
    'minMlb_2p318fb_isE_nT0p_nW1p_nB0',
    'minMlb_2p318fb_isE_nT0p_nW1p_nB1',
    'minMlb_2p318fb_isE_nT0p_nW1p_nB2',
    'minMlb_2p318fb_isE_nT0p_nW1p_nB3p',
    'minMlb_2p318fb_isM_nT0p_nW0_nB0',
    'minMlb_2p318fb_isM_nT0p_nW0_nB1',
    'minMlb_2p318fb_isM_nT0p_nW0_nB2',
    'minMlb_2p318fb_isM_nT0p_nW0_nB3p',
    'minMlb_2p318fb_isM_nT0p_nW1p_nB0',
    'minMlb_2p318fb_isM_nT0p_nW1p_nB1',
    'minMlb_2p318fb_isM_nT0p_nW1p_nB2',
    'minMlb_2p318fb_isM_nT0p_nW1p_nB3p'
]

tt_signals = {
    'TTM0700' : 'TTM700',
    'TTM0800' : 'TTM800',
    'TTM0900' : 'TTM900',
    'TTM1000' : 'TTM1000',
    'TTM1100' : 'TTM1100',
    'TTM1200' : 'TTM1200',
    'TTM1300' : 'TTM1300',
    'TTM1400' : 'TTM1400',
    'TTM1500' : 'TTM1500',
    'TTM1600' : 'TTM1600',
    'TTM1700' : 'TTM1700',
    'TTM1800' : 'TTM1800',
}

bb_signals = {
    'BBM0700' : 'BBM700',
    'BBM0800' : 'BBM800',
    'BBM0900' : 'BBM900',
    'BBM1000' : 'BBM1000',
    'BBM1100' : 'BBM1100',
    'BBM1200' : 'BBM1200',
    'BBM1300' : 'BBM1300',
    'BBM1400' : 'BBM1400',
    'BBM1500' : 'BBM1500',
    'BBM1600' : 'BBM1600',
    'BBM1700' : 'BBM1700',
    'BBM1800' : 'BBM1800',
}

rename_signals = {
    'TTM0700' : 'TpTp_M-0700',
    'TTM0800' : 'TpTp_M-0800',
    'TTM0900' : 'TpTp_M-0900',
    'TTM1000' : 'TpTp_M-1000',
    'TTM1100' : 'TpTp_M-1100',
    'TTM1200' : 'TpTp_M-1200',
    'TTM1300' : 'TpTp_M-1300',
    'TTM1400' : 'TpTp_M-1400',
    'TTM1500' : 'TpTp_M-1500',
    'TTM1600' : 'TpTp_M-1600',
    'TTM1700' : 'TpTp_M-1700',
    'TTM1800' : 'TpTp_M-1800',
    'BBM0700' : 'BpBp_M-0700',
    'BBM0800' : 'BpBp_M-0800',
    'BBM0900' : 'BpBp_M-0900',
    'BBM1000' : 'BpBp_M-1000',
    'BBM1100' : 'BpBp_M-1100',
    'BBM1200' : 'BpBp_M-1200',
    'BBM1300' : 'BpBp_M-1300',
    'BBM1400' : 'BpBp_M-1400',
    'BBM1500' : 'BpBp_M-1500',
    'BBM1600' : 'BpBp_M-1600',
    'BBM1700' : 'BpBp_M-1700',
    'BBM1800' : 'BpBp_M-1800',
}

rename_uncerts_dict = {
    'ht_reweight' : 'jsf'
}

# dict_uncerts = {
#     'TTbar' : 1.10,
#     'WJets' : 1.10,
#     'QCD' : 2.0,
#     'DYJets' : 1.2,
#     'SingleTop' : 1.2,
# }

samples = [
    'TTbar',
    'WJets',
    'QCD',
    'DYJets',
    'SingleTop',
    'Diboson',
    'Run2015'
]

x_axis_lim="m_{T} [GeV]"
y_axis_lim="Upper limit on #sigma(pp #rightarrow TT)[pb]"

all_regions = [
    'SignalRegion2b_Mu45',
    'SignalRegion1b_Mu45',
    # 'SidebandRegion_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion1b_El45',
    # 'SidebandRegion_El45',
]

def unselect_theory_uncert_single_sig(list_region):
    def sel_sig(signal):
        def tmp(wrp):
            if (sensitivity.default_selection(wrp)
                    and (any(a in os.path.basename(wrp.file_path) for a in samples)
                        or any(rename_signals.get(signal, '')+f in wrp.file_path for f in sensitivity.final_states_to_use))
                    and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))
                    and common_plot.unselect_theory_uncert(wrp)):
                return True
        return tmp
    return sel_sig

def rename_uncerts(wrps):
    for w in wrps:
        for b, a in rename_uncerts_dict.iteritems():
            if b in w.sys_info:
                w.sys_info = w.sys_info.replace(b, a)
        yield w

def split_scalevar_uncerts(wrps):
    for w in wrps:
        if 'ScaleVar' in w.sys_info:
            w.sys_info = w.sys_info+'_'+w.sample
        yield w

def rename_samples(wrps):
    for w in wrps:
        if w.sample in ['TTbar', 'TTbar_split', 'SingleTop']:
            w.sample = 'top__'+w.sample
        if w.sample in ['WJets', 'DYJets', 'Diboson']:
            w.sample = 'ewk__'+w.sample
        if w.sample == 'QCD':
            w.sample = 'qcd'
        yield w

def remove_nom_wrps(wrps):
    for w in wrps:
        if w.sys_info:
            yield w

def loader_hook(wrps, brs):
    wrps = sensitivity.loader_hook(brs)(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    wrps = gen.group(wrps, lambda w: w.in_file_path)
    wrps = common_plot.make_uncertainty_histograms(wrps, None, uncerts, False, False)
    wrps = list(w for ws in wrps for w in ws)
    # wrps = remove_nom_wrps(wrps)
    wrps = rename_uncerts(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    return wrps

def filter_func_postfit_morphed(wrp):
    if not 'MLE' in wrp.file_path:
        # if 'DATA' in wrp.in_file_path:
        #     print wrp.file_path, wrp.in_file_path
        return 'DATA' in wrp.in_file_path
    else:
        # print wrp.file_path, wrp.in_file_path
        return True

def loader_hook_postfit_morphed(wrps):
    wrps = add_wrp_info(wrps)
    wrps = mod_in_file_path(wrps)
    wrps = common_plot.mod_legend(wrps)
    return wrps

def plot_grouper_postfit_morphed(wrps):
    wrps = sorted(wrps, key=lambda w: w.in_file_path.split('__')[0])
    return gen.group(wrps, key_func=lambda w: w.in_file_path.split('__')[0])

def mod_in_file_path(wrps):
    for w in wrps:
        yield varial.operations.add_wrp_info(
            w,
            in_file_path=lambda w: w.in_file_path.split('__')[0]
        )

def add_wrp_info(wrps, sig_ind=None):
    def get_samplename(wrp):
        if 'MLE' in wrp.file_path:
            return w.in_file_path.split('__')[1]
        else:
            return 'Data'
        
    for w in wrps:
        yield varial.operations.add_wrp_info(
            w,
            sample=get_samplename,
            legend=get_samplename,
            # in_file_path=lambda w: w.in_file_path if 'jug-file' not in w.file_path else batch_tp_infilepath,
            # is_signal=lambda w: any(s in w.file_path for s in sig_ind),
            is_data=lambda w: 'DATA' in w.in_file_path,
            # variable=lambda w: w.in_file_path.split('/')[-1],
            # sys_info=vlq_common.get_sys_info,
            # is_set=lambda _: True,
        )

def plotter_factory_postfit_morphed(**args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_postfit_morphed
        kws['plot_grouper'] = plot_grouper_postfit_morphed
        kws['plot_setup'] = lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True)
        kws['stack_setup'] = lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['canvas_post_build_funcs'] = common_plot.get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp


def create_rootfiles(br_string, brs, signal, pattern=pattern_tt, sys_pat=sys_pat_tt, filter_keyfunc=None, categories=all_regions):
    filter_func = unselect_theory_uncert_single_sig(categories)(signal) if not filter_keyfunc else filter_keyfunc
    return [
        varial.tools.HistoLoader(
            name='HistoLoader',
            pattern=pattern,
            filter_keyfunc=filter_func,
            hook_loaded_histos=lambda w: loader_hook(w, brs)
        ),
        varial.tools.HistoLoader(
            name='HistoLoaderSys',
            pattern=sys_pat+pattern,
            filter_keyfunc=filter_func,
            hook_loaded_histos=lambda w: remove_nom_wrps(loader_hook(w, brs))
        ),
        ThetaLimits(
            name='HiggsTagTemplates',
            # input_path= '../HistoLoader',
            cat_key=lambda w: w.category,
            sys_key=lambda w: w.sys_info,
            # hook_loaded_histos=loader_hook_rename_uncerts,
            # name= 'ThetaLimitsSplit'+str(ind),
            # asymptotic=varial.settings.asymptotic,
            # brs=brs,
            make_root_files_only=True,
            theta_root_file_name='HiggsTagTemplate_'+br_string+'_'+signal,
            model_func=None,
            # do_postfit=False,
        )
    ]


def mk_limit_tc(brs, input_path, model_func, signal='', asymptotic=True):
    # def tmp():
    limits = common_sensitivity.TpTpThetaLimitsFromFile(
        name='ThetaLimit',
        input_path=input_path,
        # name= 'ThetaLimitsSplit'+str(ind),
        asymptotic=asymptotic,
        brs=brs,
        # model_func=lambda w: model_func(w, signal)
        model_func=model_func,
        calc_limits=True if signal else False
        # out_name=signal
        # do_postfit=False,
    )
    postfit = ThetaPostFitPlot(
        name='PostFit',
        input_path='../ThetaLimit'
    )
    corr_mat = CorrelationMatrix(
        input_path='../ThetaLimit',
        proc_name=signal
        )
    corr_plotter = varial.plotter.Plotter(
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
    return [limits, postfit] #, corr_mat, corr_plotter, post_loader, plotter_postfit, 
        # return tmp

def mk_bkg_only_fit(output_name, model=theta_combined_template.get_full_model):
    tc = [varial.tools.ToolChain(
        'BackgroundOnlyFit', 
        create_rootfiles('bkg_only', [], '', pattern=pattern_tt, sys_pat=sys_pat_tt) +\
        mk_limit_tc(
            [],
            ['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root',
                base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix],
            lambda w: model(w, None, lambda w: 'TpTp' not in w),
            '',
        )),
        # sensitivity.mk_tc_postfit_plot(theta_lim_path='../../ThetaLimit', pattern=pattern_tt, sys_pat=sys_pat_tt,
        #     sys_uncerts=uncerts, plots=['ST']),
        varial.tools.WebCreator()
    ]
        
    return varial.tools.ToolChain(output_name, tc)


def mk_bkg_only_fit_compare_comb(output_name):
    tc = [varial.tools.ToolChain(
            'BackgroundOnlyFitCombined', 
            create_rootfiles('bkg_only', [], '', pattern=pattern_tt, sys_pat=sys_pat_tt) +\
            mk_limit_tc(
                [],
                ['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root',
                    base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix],
                lambda w: theta_combined_template.get_full_model(w, None, lambda w: 'TpTp' not in w),
                '',
            ) +\
            sensitivity.mk_tc_postfit_plot(pattern=pattern_tt, sys_pat=sys_pat_tt,
                sys_uncerts=uncerts, plots=['ST'])+\
            [plot.mk_toolchain('PostFitMorphed', flat=True, pattern=['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root',
                base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix,
                '../ThetaLimit/ThetaMLE_.root'],
                filter_keyfunc=filter_func_postfit_morphed,
                plotter_factory=plotter_factory_postfit_morphed(),
                )]
        ),
        varial.tools.ToolChain(
            'BackgroundOnlyFitOnlyBW', 
            # create_rootfiles('bkg_only', [], '', pattern=pattern_tt, sys_pat=sys_pat_tt) +\
            mk_limit_tc(
                [],
                [base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix],
                lambda w: theta_combined_template.get_full_model(w, None, lambda w: 'TpTp' not in w),
                '',
            ) +\
            sensitivity.mk_tc_postfit_plot(pattern=pattern_tt, sys_pat=sys_pat_tt,
                sys_uncerts=uncerts, plots=['ST'])+\
            [plot.mk_toolchain('PostFitMorphed', flat=True, pattern=['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root',
                base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix,
                '../ThetaLimit/ThetaMLE_.root'],
                filter_keyfunc=filter_func_postfit_morphed,
                plotter_factory=plotter_factory_postfit_morphed(),
                )]
        ),
        varial.tools.ToolChain(
            'BackgroundOnlyFitOnlyBH', 
            create_rootfiles('bkg_only', [], '', pattern=pattern_tt, sys_pat=sys_pat_tt) +\
            mk_limit_tc(
                [],
                ['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root'],
                lambda w: theta_combined_template.get_full_model(w, None, lambda w: 'TpTp' not in w),
                '',
            ) +\
            sensitivity.mk_tc_postfit_plot(pattern=pattern_tt, sys_pat=sys_pat_tt,
                sys_uncerts=uncerts, plots=['ST'])+\
            [plot.mk_toolchain('PostFitMorphed', flat=True, pattern=['../HiggsTagTemplates/HiggsTagTemplate_bkg_only_.root',
                base_path_julie+'TTM700_bW0p5_tZ0p25_tH0p25'+file_suffix,
                '../ThetaLimit/ThetaMLE_.root'],
                filter_keyfunc=filter_func_postfit_morphed,
                plotter_factory=plotter_factory_postfit_morphed(),
                )]
        ),
        varial.tools.WebCreator()
    ]
        
    return varial.tools.ToolChainParallel(output_name, tc, n_workers=1)

def mk_ind_graphs(brs, name='LimitWithGraphs', plot_obs=True):
    return varial.tools.ToolChain(name,[
        limits.LimitGraphsNew(
            limit_path='../../ThetaLimits/*/ThetaLimit',
            plot_obs=plot_obs,
            split_mass=True,
            plot_1sigmabands=True,
            plot_2sigmabands=True,
            axis_labels=(x_axis_lim, y_axis_lim),
            ),
        varial.plotter.Plotter(
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
                common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                ],
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
                common_plot.mk_tobject_draw_func(TLatex(0.75, 0.79, "#scale[0.7]{#bf{CMS}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.67, 0.73, "#scale[0.6]{#it{Simulation}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),]
            ),

        varial.plotter.Plotter(
            name='PlotterBoxObs',
            input_result_path='../TriangleMassLimitPlots',
            filter_keyfunc=lambda w: 'obs' in w.save_name,
            plot_setup=sensitivity.plot_setup_triangle('col'),
            save_name_func=lambda w: w.save_name,
            canvas_post_build_funcs=[sensitivity.DrawLess700(),
                common_plot.mk_tobject_draw_func(TLatex(0.75, 0.79, "#scale[0.7]{#bf{CMS}}")),
                # common_plot.mk_tobject_draw_func(TLatex(0.66, 0.73, "#scale[0.6]{#it{Preliminary}}")),
                common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),]
            ),
        ])

def limits_only_boostH(br_str, brs, asymptotic=True, model=theta_combined_template.get_full_model):
    return varial.tools.ToolChainParallel(
        'ThetaLimits', list(varial.tools.ToolChain(
            sig, 
            create_rootfiles(br_str, brs, sig, pattern=pattern_tt, sys_pat=sys_pat_tt, categories=all_regions+['SidebandRegion_Mu45', 'SidebandRegion_El45']) +\
            mk_limit_tc(
                brs,
                ['../HiggsTagTemplates/HiggsTagTemplate_'+br_str+'_'+sig+'.root'],
                model,
                sig,
                asymptotic
            ))
        for sig, file_path in tt_signals.iteritems())
    )

def limits_only_boostW(br_str, brs, asymptotic=True, model=theta_combined_template.get_full_model):
    return varial.tools.ToolChainParallel(
        'ThetaLimits', list(varial.tools.ToolChain(
            sig, 
            mk_limit_tc(
                brs,
                [base_path_julie+file_path+'_'+br_str+file_suffix],
                model,
                sig,
                asymptotic
            ))
        for sig, file_path in tt_signals.iteritems())
    )

def limits_comb(br_str, brs, asymptotic=True, model=theta_combined_template.get_full_model):
    return varial.tools.ToolChainParallel(
        'ThetaLimits', list(varial.tools.ToolChain(
            sig, 
            create_rootfiles(br_str, brs, sig, pattern=pattern_tt, sys_pat=sys_pat_tt) +\
            mk_limit_tc(
                brs,
                ['../HiggsTagTemplates/HiggsTagTemplate_'+br_str+'_'+sig+'.root',
                base_path_julie+file_path+'_'+br_str+file_suffix],
                model,
                sig,
                asymptotic
            ))
        for sig, file_path in tt_signals.iteritems())
    )

def mk_limit_list(output_name, lim_func, asymptotic=True, model=theta_combined_template.get_full_model):
    # def tmp():
    limit_list = []
    for br_str, brs in br_list_tt:
        # if ind > 5: break
        tc = []
        tc.append(lim_func(br_str, brs, asymptotic, model=model))
        tc.append(mk_ind_graphs(brs, 'LimitsWithGraphs', True))
        tc.append(mk_ind_graphs(brs, 'LimitsWithGraphsNoObs', False))
        limit_list.append(
            varial.tools.ToolChain('Limit_'+br_str, tc))

    ind_limits = varial.tools.ToolChainParallel('Ind_Limits', limit_list, n_workers=1)

    tr_list = mk_triangle(list('../../Ind_Limits/Limit_%s/LimitsWithGraphs/LimitCurvesCompared' % i[0]
                for i in br_list_tt if i[0] not in ['bW0p5_tZ0p25_tH0p25', 'bW0p0_tZ0p5_tH0p5']))
    return varial.tools.ToolChain(output_name, [
        ind_limits,
        mk_bkg_only_fit('BkgFit', model=model),
        tr_list,
        # mk_tc_tex(output_name),
        varial.tools.WebCreator()
        ])
    # return tmp
    # return tmp

def mk_tc_tex(source_dir):
    tc_tex_an = [
        tex_content.mk_plot_ind(
            (
                ('limit_nominal', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_tHtZ_0p5', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p0_tZ0p5_tH0p5/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_tH_1p0', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p0_tZ0p0_tH1p0/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_bW_1p0', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW1p0_tZ0p0_tH0p0/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('triangle_lim_exp', os.path.join(base_path, source_dir)+'/LimitTriangle/PlotterBoxExp/lim_exp_lin.pdf'),
                ('triangle_lim_obs', os.path.join(base_path, source_dir)+'/LimitTriangle/PlotterBoxObs/lim_obs_lin.pdf'),
                ('postfit', os.path.join(base_path, source_dir)+'/BkgFit/BackgroundOnlyFit/PostFit/cnv_post_fit_.pdf'),
            ), name='LimitPlots'),
        tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/ThetaLimits', 'SysTabs', mass_points=['TTM0700', 'TTM1200', 'TTM1700'], regions=regions),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/EffTableCompFSPAS/count_table_content.tex', name='EffTableCompFS_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/BackgroundOnlyFitNoTheory/CR/PostFitPlots/CountTablePostFitPAS/count_table_content.tex', name='CountTablePostFit_'+name),
        
    ]
    tc_tex_pas = [
        tex_content.mk_plot_ind(
            (
                ('limit_nominal', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_tHtZ_0p5', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p0_tZ0p5_tH0p5/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_tH_1p0', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p0_tZ0p0_tH1p0/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('limit_bW_1p0', os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW1p0_tZ0p0_tH0p0/LimitsWithGraphs/LimitCurvesCompared/lim_graph_log.pdf'),
                ('triangle_lim_exp', os.path.join(base_path, source_dir)+'/LimitTriangle/PlotterBoxExp/lim_exp_lin.pdf'),
                ('triangle_lim_obs', os.path.join(base_path, source_dir)+'/LimitTriangle/PlotterBoxObs/lim_obs_lin.pdf'),
                ('postfit', os.path.join(base_path, source_dir)+'/BkgFit/BackgroundOnlyFit/PostFit/cnv_post_fit_.pdf'),
            ), name='LimitPlots'),
        # tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/ThetaLimits', 'SysTabs', mass_points=['TTM0700', 'TTM1200', 'TTM1700'], regions=regions),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/EffTableCompFSPAS/count_table_content.tex', name='EffTableCompFS_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/BackgroundOnlyFitNoTheory/CR/PostFitPlots/CountTablePostFitPAS/count_table_content.tex', name='CountTablePostFit_'+name),
        
    ]
    # # if name == 'TopPtAndHTReweighting':
    # #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
    # #     tc_tex_pas += [tex_content.mk_autoContentLimitsVarSize(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
    # # else:
    # #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions', mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
    # #     tc_tex_pas += [tex_content.mk_autoContentLimitsVarSize(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
    tc_tex_pas = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexAN', tc_tex_an),
        varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-16-343/trunk/', src='../TexAN/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, name='CopyToolAN'),
        varial.tools.ToolChain('TexPaper', tc_tex_pas),
        varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:PAS-Dir/notes/B2G-16-024/trunk/', src='../TexPaper/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, name='CopyToolPaper'),
        ])
    return tc_tex_pas

def mk_all_templates(source_dir):
    limit_list = []
    for br_str, brs in br_list_tt:
        # if ind > 5: break
        tc = []
        tc.append(varial.tools.ToolChainParallel(
            'ThetaLimits', list(varial.tools.ToolChain(
                sig, 
                create_rootfiles(br_str, brs, sig, pattern=pattern_tt, sys_pat=sys_pat_tt))
            for sig in tt_signals.keys())
        ))
        limit_list.append(
            varial.tools.ToolChain('Limit_'+br_str, tc))
    for br_str, brs in br_list_bb:
        # if ind > 5: break
        tc = []
        tc.append(varial.tools.ToolChainParallel(
            'ThetaLimits', list(varial.tools.ToolChain(
                sig, 
                create_rootfiles(br_str, brs, sig, pattern=pattern_bb, sys_pat=sys_pat_bb))
            for sig in bb_signals.keys())
        ))
        limit_list.append(
            varial.tools.ToolChain('Limit_'+br_str, tc))

    ind_limits = varial.tools.ToolChainParallel(source_dir, limit_list, n_workers=1)
    return ind_limits

if __name__ == '__main__':
    output_name = sys.argv[1]
    if len(sys.argv) > 2:
        version = sys.argv[2]
        if version == 'v24':
            base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
                'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24'
            pattern_tt = [base_path+'/Run8_withHighMassTTbarSample/'\
                'RunAnalysis/HTReweighting/TreeProject/TreeProjector/*.root',
                base_path+'/Run8_withHighMassTTbarSample/'\
                'RunAnalysis/HTReweighting/TreeProject/TreeProjectorDiboson/*.root']
            sys_path = base_path+'/Run8_withHighMassTTbarSample/'\
                'RunAnalysis/HTReweighting/TreeProject/SysTreeProjectors'
            sys_pat_tt = list(sys_path+'/%s*/*.root'% i for i in uncerts) + list(sys_path+'Diboson/%s*/*.root'% i for i in uncerts)

    # all_tools = mk_limit_list()
    # varial.tools.Runner(varial.tools.ToolChainParallel(output_name, [
    #     # mk_limit_list('LimitsBoostedHOnly', limits_only_boostH, False),
    #     mk_limit_list('LimitsNoExtraUncert', limits_comb, False, model=theta_combined_template.get_full_model),
    #     mk_limit_list('LimitsAntiCorrExUncert', limits_comb, False, model=theta_combined_template.get_model_ex_anticorr_chan),
    #     mk_limit_list('LimitsCorrExUncert', limits_comb, False, model=theta_combined_template.get_model_ex_corr_chan),
    #     mk_limit_list('LimitsAntiCorrBtagExUncert', limits_comb, False, model=theta_combined_template.get_model_ex_anticorr_btag),
    #     mk_limit_list('LimitsCorrBtagExUncert', limits_comb, False, model=theta_combined_template.get_model_ex_corr_btag),
    #     varial.tools.WebCreator()
    #     ], n_workers=1), default_reuse=True)
    # varial.tools.Runner(mk_bb_templates(output_name), default_reuse=True)
    varial.tools.Runner(mk_all_templates(output_name), default_reuse=True)
    # varial.tools.Runner(mk_bkg_only_fit_compare_comb(output_name), default_reuse=True)
    # varial.tools.Runner(mk_bkg_only_fit(output_name), default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()