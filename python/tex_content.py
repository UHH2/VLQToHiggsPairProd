#!/usr/bin/env python

from varial.extensions import tex
import varial.settings
import varial.tools
import os.path

# base path
# p_base = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3'\
# '/src/UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/'
# presel_version = 'v7'
# p_prebase = p_base + 'TpTpPreselection-%s/Files_and_Plots'\
# '/Files_and_Plots_nominal/Plots/Plots/' % presel_version
# post_version = 'v4'
# p_postbase = p_base + 'TpTpFinalSelectionTreeOutput-%s/RunLimits/Histograms/' % post_version
ext = '.pdf'
target_ext = '.pdf'
varial.settings.rootfile_postfixes += ['.pdf']
mu_channel_def = 'Mu45_Baseline'
el_channel_def = 'El45_Baseline'
muel_comb_def = 'MuElComb_Baseline'
muchannel_final = 'Muon'
elchannel_final = 'Electron'

#########################################################
############ PRESELECTION N MINUS 1 PLOTS ###############
############ PRESELECTION CUTFLOW PLOTS #################
#########################################################
# p_nm1 = p_prebase + '%s/Nm1Selection/'


def get4sel(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'Nm1Selection/')
    return {
        chan+'_twoDeeCut': (
            p + 'twod_cut_hist_noIso_QCD_log' + ext,
            p + 'twod_cut_hist_noIso_TpTp_M-1200_log' + ext,
            p + 'twod_cut_hist_noIso_px_log' + ext,
            p + 'twod_cut_hist_noIso_py_log' + ext,
        ),
        chan+'_firstblock': (            
            p + 'ST_lin' + ext,
            p + 'n_ak8_lin' + ext,
            p + 'n_ak4_log' + ext,
            p + 'primary_lepton_pt_lin' + ext,
        ),
    }.items()

# img_2d_px = {
#     'twoDeeCut_pxy': (
#         (p_nm1 % muchannel) + 'twod_cut_hist_noIso_px_log' + ext,
#         (p_nm1 % muchannel) + 'twod_cut_hist_noIso_py_log' + ext,
#     ),
# }.items()

def get4cf(chan, base):
    p = os.path.join(base, 'CutflowTools/')

    return {
        chan+'_cutflow_tabular.tex':
            p + chan + '/CutflowTableTex/cutflow_tabular.tex',
        chan+'_cutflow_stack'+target_ext:
            p + chan + '/CutflowStack/cutflow_log'+ext,
    }.items()

def mk_autoContentPreSelectionNm1(base, el_channel=None, mu_channel=None):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(get4sel(muchannel, base) + get4sel(elchannel, base)),
        # dict(get4sel(muchannel, base) + get4sel(elchannel, base) + img_2d_px),
        dict(get4cf(muchannel, base) + get4cf(elchannel, base)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name='AutoContentSelection',
    )

#########################################################
############ FINAL SELECTION CONTROL PLOTS #############=
#########################################################

def get4obj(chan, base):
    histos_all = 'pt_lin', 'eta_lin', 'phi_lin', 'number_lin'
    histos_first = 'pt_1_lin', 'eta_1_lin', 'phi_1_lin', 'number_lin'
    jet_histos = 'pt_jet_lin', 'eta_jet_lin', 'phi_jet_lin', 'number_log'
    p = os.path.join(base+'/StackedAll', chan, 'PostSelection/')
    return {
        chan+'_muons'     : map((p+'MuonHists/{}'+ext).format, histos_first),
        chan+'_electrons' : map((p+'ElectronHists/{}'+ext).format, histos_first),
        chan+'_jets'      : map((p+'JetHists/{}'+ext).format, jet_histos),
        chan+'_ak8_jets'  : map((p+'SlimmedAk8Jets/{}'+ext).format, histos_all),
        # chan+'_higg_jets' : map((p+'HiggsJetsAfterSel/{}'+ext).format, histos),
        chan+'_jet_pts'   : map((p+'JetHists/{}'+ext).format, 
            ('pt_1_lin', 'pt_2_lin', 'pt_3_lin', 'pt_4_lin', )
        ),
        chan+'_ak8jet_pts'   : map((p+'SlimmedAk8Jets/{}'+ext).format, 
            ('pt_1_lin', 'pt_2_lin', 'pt_3_lin', )
        ),
        chan+'_event'     : map((p+'EventHists/{}'+ext).format, 
            ('N_PrimVertices_lin', 'N_TrueInteractions_lin', 'ST_rebin_flex_log', 'MET_own_lin', )
        ),
    }.items()

def mk_autoContentControlPlots(base, el_channel=None, mu_channel=None):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(get4obj(muchannel, base) + get4obj(elchannel, base)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name='AutoContentObjects',
    )

#########################################################
####################### DEPRECATED ######################
#########################################################
############ FINAL SELECTION HIGGS TAG PLOTS ############
#########################################################

# --TODO: implement Nm1 Plots after higgs-tags! esp. add. b-tag plots, N(higgs tags plots)
def getHiggsVar(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'PostSelection/FirstAk8SoftDropSlimmed/')
    return {
        chan+'_Nm1Var_htag': (
            p + 'Nobtag_boost_mass/n_sjbtags_medium_log' + ext,
            p + 'Noboost_mass_1b/pt_log' + ext,
            p + 'Nomass_boost_1b/mass_sj_lin' + ext,
            p + 'Nomass_boost_2b/mass_sj_lin' + ext,
        ),
        chan+'_Nm1Var_htag_only_massbtag': (
            p + 'Nobtag_boost_mass/n_sjbtags_medium_log' + ext,
            p + 'Nomass_boost_2b/mass_sj_lin' + ext,
        ),
    }.items()

def mk_autoContentFinalSelectionHiggsVar(base, el_channel=None, mu_channel=None, muel_comb=None, name='AutoContentFinalSelectionHiggsVar'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    muelcomb = muel_comb or muel_comb_def
    return varial.extensions.tex.TexContent(
        dict(getHiggsVar(muchannel, base) + getHiggsVar(elchannel, base) + getHiggsVar(muelcomb, base)),
        include_str=r'\includegraphics[width=0.38\textwidth]{%s}',
        name=name,
    )



#########################################################
######### FINAL SELECTION HT REWEIGHTING PLOTS #########=
#########################################################

# def get4sb(chan, base):
#     p_correct = os.path.join(base+'/StackedAll', chan, 'PostSelection/JetCleaningControlPlots/')
#     p_uncorrect = os.path.join(base+'/StackedAll', chan, 'PostSelection/')
#     return {
#         chan+'_jetptreweight': (
#             p_correct + 'ST_cleaned_lin' + ext,
#             p_uncorrect + 'ST_lin' + ext,
#             p_correct + 'n_ak4_cleaned_lin' + ext,
#             p_uncorrect + 'n_ak4_lin' + ext,
#             p_correct + 'pt_ak4_cleaned_lin' + ext,
#             p_uncorrect + 'pt_ld_ak4_jet_lin' + ext,
#         )}.items()

# def mk_autoContentJetPtReweight(base, el_channel=None, mu_channel=None):
#     muchannel = mu_channel or mu_channel_def
#     elchannel = el_channel or el_channel_def
#     return varial.extensions.tex.TexContent(
#         dict(get4sb(muchannel, base) + get4sb(elchannel, base)),
#         include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
#         name='AutoContentJetPtReweight',
#     )

#########################################################
########## TREEPROJECT OUTPUT NO DATA PLOTS #############
#########################################################

# def getNoDataFinalVar(chan, base):
#     p = os.path.join(base, 'HistogramsNoData/StackedAll/')
#     # print base
#     return {
#         chan+'_Nm1ak4btag': (
#             p + 'SignalRegion1b_%s/n_additional_btags_medium_lin' % chan + ext,
#             p + 'SignalRegion2b_%s/n_additional_btags_medium_lin' % chan + ext,
#             p + 'SidebandRegion_%s/n_additional_btags_medium_lin' % chan + ext,
#         ),
#         chan+'_Nm1htag': (
#             p + 'SidebandRegion_%s/n_higgs_tags_1b_med_lin' % chan + ext,
#             p + 'SignalRegion2b_%s/n_higgs_tags_2b_med_lin' % chan + ext,
#         ),
#         chan+'_st': (
#             p + 'SignalRegion1b_%s/ST_lin' % chan + ext,
#             p + 'SignalRegion2b_%s/ST_lin' % chan + ext,
#             p + 'SidebandRegion_%s/ST_lin' % chan + ext,
#         ),
#     }.items()

# def mk_autoContentNoDataFinalRegions(base, el_channel=None, mu_channel=None):
#     muchannel = mu_channel or mu_channel_def
#     elchannel = el_channel or el_channel_def
#     return varial.extensions.tex.TexContent(
#         dict(getNoDataFinalVar(muchannel, base) + getNoDataFinalVar(elchannel, base)),
#         include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
#         name='AutoContentNoDataFinalRegions',
#     )

#########################################################
####### TREEPROJECT OUTPUT SYSTEMATIC CR PLOTS ##########
#########################################################

def getSystCRPlots(chan, base):
    p = os.path.join(base, 'StackedAll/')
    # print base
    return {
        chan+'_ak4jetpt': (
            p + 'SidebandRegion_%s/pt_ld_ak4_jet_log' % chan + ext,
            p + 'SidebandRegion_%s/pt_subld_ak4_jet_log' % chan + ext,
            p + 'SidebandRegion_%s/pt_third_ak4_jet_log' % chan + ext,
            p + 'SidebandRegion_%s/pt_fourth_ak4_jet_log' % chan + ext,
        ),
        chan+'_ak8jetpt': (
            p + 'SidebandRegion_%s/pt_ld_ak8_jet_log' % chan + ext,
            p + 'SidebandRegion_%s/pt_subld_ak8_jet_log' % chan + ext,
        ),
        chan+'_stplusjets': (
            p + 'SidebandRegion_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SidebandRegion_%s/HT_rebin_flex_log' % chan + ext,
            p + 'SidebandRegion_%s/n_ak4_log' % chan + ext,
            p + 'SidebandRegion_%s/n_ak8_log' % chan + ext,
        ),
        chan+'_eventvar': (
            p + 'SidebandRegion_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SidebandRegion_%s/HT_rebin_flex_log' % chan + ext,
            p + 'SidebandRegion_%s/primary_lepton_pt_log' % chan + ext,
            p + 'SidebandRegion_%s/met_log' % chan + ext,
        ),
        chan+'_njets': (
            p + 'SidebandRegion_%s/n_ak4_log' % chan + ext,
            p + 'SidebandRegion_%s/n_ak8_log' % chan + ext,
        ),
        chan+'_stht': (
            p + 'SidebandRegion_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SidebandRegion_%s/HT_rebin_flex_log' % chan + ext,
        )
    }.items()

def mk_autoContentSystematicCRPlots(base, el_channel=None, mu_channel=None, name='AutoContentSystematicCRPlots'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getSystCRPlots(muchannel, base) + getSystCRPlots(elchannel, base)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name=name,
    )

#########################################################
### TREEPROJECT OUTPUT SYSTEMATIC COMPARISON PLOTS ######
#########################################################

def getCompSystPlots(chan, base):
    # p = os.path.join(base, 'StackedAll/')
    # print base
    return {
        chan+'_stcomp': list(
            p + '/StackedAll/SidebandRegion_%s/ST_rebin_flex_log' % chan + ext for p in base
        )
    }.items()

def mk_autoContentCompSystPlots(base, el_channel=None, mu_channel=None, name='AutoContentCompSystPlots'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getCompSystPlots(muchannel, base) + getCompSystPlots(elchannel, base)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name=name,
    )

#########################################################
########## TREEPROJECT OUTPUT N MINUS 1 PLOTS ###########
#########################################################

def getFinalVar(chan, base):
    p = os.path.join(base, 'StackedAll/')
    # print base
    return {
        chan+'_Nm1ak4btag': (
            p + 'SignalRegion1b_%s/n_additional_btags_medium_log' % chan + ext,
            p + 'SignalRegion2b_%s/n_additional_btags_medium_log' % chan + ext,
            p + 'SidebandRegion_%s/n_additional_btags_medium_log' % chan + ext,
        ),
        chan+'_Nm1htag': (
            p + 'SidebandRegion_%s/n_higgs_tags_1b_med_log' % chan + ext,
            p + 'SignalRegion2b_%s/n_higgs_tags_2b_med_log' % chan + ext,
        ),
        chan+'_st': (
            p + 'SidebandRegion_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SignalRegion1b_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SignalRegion2b_%s/ST_rebin_flex_log' % chan + ext,
        ),
        chan+'_st_sigonly': (
            p + 'SignalRegion1b_%s/ST_rebin_flex_log' % chan + ext,
            p + 'SignalRegion2b_%s/ST_rebin_flex_log' % chan + ext,
            # p + 'SidebandRegion_%s/ST_log' % chan + ext,
        ),
    }.items()

def mk_autoContentSignalControlRegion(base, el_channel=None, mu_channel=None, name='AutoContentSignalControlRegion'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getFinalVar(muchannel, base) + getFinalVar(elchannel, base)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name=name,
    )

#########################################################
########## TREEPROJECT OUTPUT COMBINED CHANNELS #########
#########################################################

def getCRSplitComb(base_split, base_comb, el_chan, mu_chan):
    # print base
    return {
        'st_split_comb': (
            os.path.join(base_split, 'SidebandRegion_%s/ST_rebin_flex_log' % mu_chan + ext),
            os.path.join(base_split, 'SidebandRegion_%s/ST_rebin_flex_log' % el_chan + ext),
            os.path.join(base_comb, 'SidebandRegion/ST_rebin_flex_log' + ext),
        ),
        'st_split': (
            os.path.join(base_split, 'SidebandRegion_%s/ST_rebin_flex_log' % mu_chan + ext),
            os.path.join(base_split, 'SidebandRegion_%s/ST_rebin_flex_log' % el_chan + ext),
            # os.path.join(base_comb, 'SidebandRegion/ST_rebin_flex_log' + ext),
        ),
    }.items()

def mk_autoContentControlRegion(base_split, base_comb, el_chan, mu_chan, name='AutoContentSignalControlRegionCombined'):
    return varial.extensions.tex.TexContent(
        dict(getCRSplitComb(base_split, base_comb, el_chan, mu_chan)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name=name,
    )

#########################################################
####### TREEPROJECT MORE OUTPUT COMBINED CHANNELS #######
#########################################################

def getFinalVarCombinedMore(base):
    # print base
    return {
        'all_st': (
            os.path.join(base, 'SidebandRegion/ST_rebin_flex_log' + ext),
            os.path.join(base, 'SignalRegion1b/ST_rebin_flex_log' + ext),
            os.path.join(base, 'SignalRegion2b/ST_rebin_flex_log' + ext),
        ),
        'st_sigonly': (
            os.path.join(base, 'SignalRegion1b/ST_rebin_flex_log' + ext),
            os.path.join(base, 'SignalRegion2b/ST_rebin_flex_log' + ext),
        ),
        'baseline_control_plots_all': (
            os.path.join(base, 'BaseLineSelection/primary_lepton_pt_lin' + ext),
            os.path.join(base, 'BaseLineSelection/met_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak4_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak8_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/HT_rebin_flex_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_ak4_log' + ext),
        ),
        'baseline_control_plots_met': (
            os.path.join(base, 'BaseLineSelection/primary_lepton_pt_lin' + ext),
            os.path.join(base, 'BaseLineSelection/met_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak4_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak8_jet_lin' + ext),
        ),
        'baseline_control_plots_leps': (
            os.path.join(base, 'BaseLineSelection/primary_muon_pt_lin' + ext),
            os.path.join(base, 'BaseLineSelection/primary_electron_pt_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak4_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak8_jet_lin' + ext),
        ),
        'baseline_control_plots': (
            os.path.join(base, 'BaseLineSelection/HT_rebin_flex_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_ak4_log' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak4_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak8_jet_lin' + ext),
        ),
        'baseline_control_plots_withHiggsTag': (
            os.path.join(base, 'BaseLineSelection/HT_rebin_flex_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_ak4_log' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak4_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/pt_ld_ak8_jet_lin' + ext),
            os.path.join(base, 'BaseLineSelection/nobtag_boost_mass_nsjbtags_log' + ext),
            os.path.join(base, 'BaseLineSelection/nomass_boost_2b_mass_lin' + ext),
        ),
        'baseline_control_plots_ht_nak4': (
            os.path.join(base, 'BaseLineSelection/HT_rebin_flex_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_ak4_log' + ext),
        ),
        'baseline_control_plots_hhiggsvar': (
            os.path.join(base, 'BaseLineSelection/nobtag_boost_mass_nsjbtags_log' + ext),
            os.path.join(base, 'BaseLineSelection/nomass_boost_2b_mass_lin' + ext),
        ),
        'baseline_control_plots_hhiggsvar_more': (
            os.path.join(base, 'BaseLineSelection/nobtag_boost_mass_nsjbtags_log' + ext),
            # os.path.join(base, 'BaseLineSelection/pt_log' + ext),
            os.path.join(base, 'BaseLineSelection/nomass_boost_1b_mass_lin' + ext),
            os.path.join(base, 'BaseLineSelection/nomass_boost_2b_mass_lin' + ext),
        ),
        'nminus1_plots_withak4btag': (
            os.path.join(base, 'BaseLineSelection/n_additional_btags_medium_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_higgs_tags_1b_med_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_higgs_tags_2b_med_log' + ext),
        ),
        'nminus1_plots': (
            # os.path.join(base, 'BaseLineSelection/n_additional_btags_medium_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_higgs_tags_1b_med_log' + ext),
            os.path.join(base, 'BaseLineSelection/n_higgs_tags_2b_med_log' + ext),
        ),
    }.items()

def mk_autoContentSignalControlRegionCombinedMore(base, name='AutoContentSignalControlRegionCombined', size='0.41'):
    return varial.extensions.tex.TexContent(
        dict(getFinalVarCombinedMore(base)),
        include_str=r'\includegraphics[width='+size+r'\textwidth]{%s}',
        name=name,
    )

#########################################################
####### TREEPROJECT MORE OUTPUT COMBINED CHANNELS #######
#########################################################

def getHiggsVarCombinedMore(base):
    # print base
    return {
        'baseline_control_plots_hhiggsvar': (
            os.path.join(base, 'BaseLineSelection/nobtag_boost_mass_nsjbtags_log' + ext),
            os.path.join(base, 'BaseLineSelection/nomass_boost_2b_mass_lin' + ext),
        ),
    }.items()

def mk_autoContentHiggsVarCombinedMore(base, name='AutoContentSignalControlRegionCombined', size='0.41'):
    return varial.extensions.tex.TexContent(
        dict(getHiggsVarCombinedMore(base)),
        include_str=r'\includegraphics[width='+size+r'\textwidth]{%s}',
        name=name,
    )


#########################################################
############## TREEPROJECT OUTPUT LIMITS ################
############ TREEPROJECT OUTPUT SYSTEMATICS #############
#########################################################

def getLimPlotsAll(base):
    # p_lim = os.path.join(base, 'LimitsSyst/Ind_Limits/Limit0/{0}/Limit{0}')
    return {
        'Limits': (
            os.path.join(base, 'LimitsAllUncertsOnlyEl/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
            os.path.join(base, 'LimitsAllUncertsOnlyMu/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
        ),
        'triangle_lim_both_box': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/LimitTriangle/PlotterBox/lim_exp_lin' + ext),
            os.path.join(base, 'LimitsAllUncertsAllRegions/LimitTriangle/PlotterBox/lim_obs_lin' + ext),
        ),
        'triangle_plus_single_lim': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
            os.path.join(base, 'LimitsAllUncertsAllRegions/LimitTriangle/PlotterBox/lim_obs_lin' + ext),
        ),
        'Postfit-all': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-0700/PostFit/cnv_post_fit_TpTp_M-0700' + ext),
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-1200/PostFit/cnv_post_fit_TpTp_M-1200' + ext),
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-1700/PostFit/cnv_post_fit_TpTp_M-1700' + ext),
        ),
    }

def getSingleLimPlotLarge(base):
    # p_lim = os.path.join(base, 'LimitsSyst/Ind_Limits/Limit0/{0}/Limit{0}')
    return {
        'Limits_comb_only': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
        ),
        'triangle_lim_obs_box': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/LimitTriangle/PlotterBox/lim_obs_lin' + ext),
        ),
        'triangle_lim_exp_box': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/LimitTriangle/PlotterBox/lim_exp_lin' + ext),
        ),
        'Postfit-M0700': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-0700/PostFit/cnv_post_fit_TpTp_M-0700' + ext),
        ),
        'Postfit-M1200': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-1200/PostFit/cnv_post_fit_TpTp_M-1200' + ext),
        ),
        'Postfit-M1700': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/TpTp_M-1700/PostFit/cnv_post_fit_TpTp_M-1700' + ext),
        ),
    }

def getLimPlotsSingle(base, prefix=''):
    # p_lim = os.path.join(base, 'LimitsSyst/Ind_Limits/Limit0/{0}/Limit{0}')
    tmp_dict = {
        'Limits_'+prefix: (
            os.path.join(base, prefix+'/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
        ) if prefix else {}
    }
    return tmp_dict

import varial.extensions.limits as limits

def my_mod_sys_table(table):
    def find_column_string(line, name):
        columns = line.split(' & ')
        indizes = list(i for i, a in enumerate(columns) if name in a)
        return indizes

    def remove_column(line, indizes):
        if r'\hline' in line:
            return line
        columns = line.split(' & ')
        # print columns
        new_columns = filter(lambda w: w[0] not in indizes, enumerate(columns))
        new_columns = zip(*new_columns)[1]
        new_columns = ' & '.join(new_columns)
        if not new_columns.endswith(r'\\'):
            new_columns += r'\\'
        return new_columns

    table = limits.tex_table_mod(table, [
        ('(gauss) ', '  '),
        ('TpTp_', ''),
        (' (s) ', ''),
        ('process / nusiance parameter', 'pr./ns. par.'),
    ] + limits.tex_table_mod_list)
    lines = table.split('\n')
    indizes = find_column_string(lines[1], 'rate') + find_column_string(lines[1], 'luminosity')\
        + find_column_string(lines[3], '---')
        # + find_column_string(lines[1], 'el trg+id') + find_column_string(lines[1], 'mu trg+id')
    for i, line in enumerate(lines):
        lines[i] = remove_column(line, indizes)
    table = '\n'.join(lines)
    return table

def find_sig_line(table, signal_ind):
    lines = table.split('\n')
    signal = ''
    rest = ''
    for l in lines[:-1]:
        columns = l.split(' & ')
        if signal_ind in columns[0]:
            signal = l
        else:
            rest += l + '\n'
    return signal, rest

# def get(table, signal_ind):
#     lines = table.split('\n')
#     signal = ''
#     rest = ''
#     for l in lines[:-1]:
#         columns = l.split(' & ')
#         if signal_ind in columns[0]:
#             signal = l
#         else:
#             rest += l + '\n'
#     return signal, rest



def getSysTab(chan, base, mass_points, mod=my_mod_sys_table):
    p_lim = os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/ThetaLimits/{0}/ThetaLimit')
    new_files = []
    # if mod:
    for region in ['SidebandRegion', 'SignalRegion1b', 'SignalRegion2b']:
        new_table = ''
        for mass in mass_points:
            filename = p_lim.format(mass)+'/sysrate_tables_{0}_{1}.tex'.format(region, chan)
            # print filename
            with open(filename) as f:
                cont = f.read()
            sig, other = find_sig_line(cont, 'TpTp')
            if not new_table:
                new_table = other
                new_table += sig + '\n'
            else:
                new_table += sig + '\n'
        new_table += r'\hline'+'\n'
        new_table += r'\end{tabular}\\'
        with open(filename.replace('.tex', '_mod.tex'), 'w') as f:
            # print mod(cont)
            f.write(mod(new_table))
        new_files.append(filename.replace('.tex', '_mod.tex'))

    return {
        chan+'_side_sys_tab.tex':
            new_files[0],
        chan+'_sig1b_sys_tab.tex':
            new_files[1],
        chan+'_sig2b_tab.tex':
            new_files[2],
    }.items()

def mk_autoContentLimits(base, el_channel=None, mu_channel=None, name='AutoContentLimits', prefix='', mass_points=None, get_sys_tab=True):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    lim_dict = getLimPlotsSingle(base, prefix) if prefix else getLimPlotsAll(base)
    tab_dict = dict(getSysTab(muchannel, base, mass_points) + getSysTab(elchannel, base, mass_points)) if get_sys_tab else {}
    return varial.extensions.tex.TexContent(
        lim_dict,
        tab_dict,
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name=name,
    )

def mk_autoContentLimitsLarge(base, el_channel=None, mu_channel=None, name='AutoContentLimits', mass_points=None, get_sys_tab=True):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    lim_dict = getSingleLimPlotLarge(base)
    tab_dict = dict(getSysTab(muchannel, base, mass_points) + getSysTab(elchannel, base, mass_points)) if get_sys_tab else {}
    return varial.extensions.tex.TexContent(
        lim_dict,
        tab_dict,
        include_str=r'\includegraphics[width=0.6\textwidth]{%s}',
        name=name,
    )



#########################################################
############ TREEPROJECT OUTPUT EFF COUNTS ##############
#########################################################

def getEffCount(filepath, mod=None):
    path = filepath
    if mod:
        with open(filepath) as f:
            cont = f.read()
        with open(filepath.replace('.tex', '_mod.tex'), 'w') as f:
            f.write(mod(cont))
        path = path.replace('.tex', '._mod.tex') 

    return {
        'count_table_content.tex': path
    }.items()

def mk_autoEffCount(filepath, mod=None, name='AutoEffCount'):
    return varial.extensions.tex.TexContent(
        plain_files=dict(getEffCount(filepath, mod)),
        include_str=r'\includegraphics[width=0.41\textwidth]{%s}',
        name=name,
    )


###############################################################################


################################################################# toolchain ###
def make_tex_content():
    # return varial.tools.ToolChainParallel(
    tc = varial.tools.ToolChain('TexCopy', [
            varial.tools.ToolChain(
                'Tex', 
                [
                    mk_autoContentSignalControlRegion(p_postbase),
                    mk_autoContentControlPlots(p_prebase),
                    mk_autoContentFinalSelectionHiggsVar(p_prebase),
                    mk_autoContentPreSelectionNm1(p_prebase),
                    mk_autoContentJetPtReweight(p_prebase),
                ]
            ),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=['*.svn'], use_rsync=True)
        ])
    return tc

import time

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    # final_dir = sys.argv[2]
    all_tools = make_tex_content()
    varial.tools.Runner(all_tools, default_reuse=False)
