#!/usr/bin/env python

from varial.extensions import tex
import varial.settings
import varial.tools
import os.path

# base path
p_base = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/CMSSW_7_4_15_patch1'\
'/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'
presel_version = 'v7'
p_prebase = p_base + 'TpTpPreselection-%s/Files_and_Plots'\
'/Files_and_Plots_nominal/Plots/Plots/' % presel_version
post_version = 'v3'
p_postbase = p_base + 'TpTpFinalSelectionTreeOutput-%s/RunLimits/Histograms/' % post_version
ext = '.pdf'
target_ext = '.pdf'
varial.settings.rootfile_postfixes += ['.pdf']
muchannel = 'Mu45'
elchannel = 'El45'
muchannel_final = 'Muon'
elchannel_final = 'Electron'

######################################################## AutoContentObjects ###
def get4obj(chan, base):
    histos_all = 'pt_lin', 'eta_lin', 'phi_lin', 'number_lin'
    histos_first = 'pt_1_lin', 'eta_1_lin', 'phi_1_lin', 'number_lin'
    jet_histos = 'pt_jet_lin', 'eta_jet_lin', 'phi_jet_lin', 'number_lin'
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
            ('N_PrimVertices_lin', 'N_TrueInteractions_lin', 'ST_lin', 'MET_own_lin', )
        ),
    }.items()

def mk_autoContentObjects(base):
    return varial.extensions.tex.TexContent(
        dict(get4obj(muchannel, base) + get4obj(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name='AutoContentObjects',
    )


##################################################### AutoContentFinalSelectionHiggsVar ###

# --TODO: implement Nm1 Plots after higgs-tags! esp. add. b-tag plots, N(higgs tags plots)
def getHiggsVar(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'NoAk8PtCut/FirstAk8SoftDropSlimmed/')
    return {
        chan+'_Nm1Var_htag': (
            p + 'Nobtag_boost_mass/n_sjbtags_medium_lin' + ext,
            p + 'Noboost_mass_1b/pt_log' + ext,
            p + 'Nomass_boost_1b/mass_sj_log' + ext,
            p + 'Nomass_boost_2b/mass_sj_log' + ext,
        ),
    }.items()

def mk_autoContentFinalSelectionHiggsVar(base):
    return varial.extensions.tex.TexContent(
        dict(getHiggsVar(muchannel, base) + getHiggsVar(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name='AutoContentFinalSelectionHiggsVar',
    )

##################################################### AutoContentSignalControlRegion ###

def getFinalVar(chan, base):
    p = os.path.join(base, 'Histograms/StackedAll/')
    # print base
    return {
        chan+'_Nm1ak4btag': (
            p + 'SignalRegion1b_%s/n_additional_btags_medium_lin' % chan + ext,
            p + 'SignalRegion2b_%s/n_additional_btags_medium_lin' % chan + ext,
            p + 'SidebandRegion_%s/n_additional_btags_medium_lin' % chan + ext,
        ),
        chan+'_Nm1htag': (
            p + 'SidebandRegion_%s/n_higgs_tags_1b_med_lin' % chan + ext,
            p + 'SignalRegion2b_%s/n_higgs_tags_2b_med_lin' % chan + ext,
        ),
        chan+'_st': (
            p + 'SignalRegion1b_%s/ST_lin' % chan + ext,
            p + 'SignalRegion2b_%s/ST_lin' % chan + ext,
            p + 'SidebandRegion_%s/ST_lin' % chan + ext,
        ),
    }.items()

def mk_autoContentSignalControlRegion(base):
    return varial.extensions.tex.TexContent(
        dict(getFinalVar(muchannel, base) + getFinalVar(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name='AutoContentSignalControlRegion',
    )



###################################################### AutoContentSelection ###
p_nm1 = p_prebase + '%s/Nm1Selection/'


def get4sel(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'Nm1Selection/')
    return {
        chan+'_twoDeeCut': (
            p + 'twod_cut_hist_noIso_QCD_lin' + ext,
            p + 'twod_cut_hist_noIso_TpTp_M-1200_lin' + ext,
            p + 'twod_cut_hist_noIso_px_log' + ext,
            p + 'twod_cut_hist_noIso_py_log' + ext,
        ),
        chan+'_firstblock': (            
            p + 'ST_lin' + ext,
            p + 'n_ak8_lin' + ext,
            p + 'pt_ld_ak8_jet_lin' + ext,
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
    print p

    return {
        chan+'_cutflow_tabular.tex':
            p + chan + '/CutflowTableTex/cutflow_tabular.tex',
        chan+'_cutflow_stack'+target_ext:
            p + chan + '/CutflowStack/cutflow_log'+ext,
    }.items()

def mk_autoContentSelection(base):
    return varial.extensions.tex.TexContent(
        dict(get4sel(muchannel, base) + get4sel(elchannel, base)),
        # dict(get4sel(muchannel, base) + get4sel(elchannel, base) + img_2d_px),
        dict(get4cf(muchannel, base) + get4cf(elchannel, base)),
        include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
        name='AutoContentSelection',
    )


####################################################### AutoContentJetPtReweight ###
def get4sb(chan, base):
    p_correct = os.path.join(base+'/StackedAll', chan, 'PostSelection/JetCleaningControlPlots/')
    p_uncorrect = os.path.join(base+'/StackedAll', chan, 'PostSelection/')
    return {
        chan+'_jetptreweight': (
            p_correct + 'ST_cleaned_lin' + ext,
            p_uncorrect + 'ST_lin' + ext,
            p_correct + 'n_ak4_cleaned_lin' + ext,
            p_uncorrect + 'n_ak4_lin' + ext,
            p_correct + 'pt_ak4_cleaned_lin' + ext,
            p_uncorrect + 'pt_ld_ak4_jet_lin' + ext,
        )}.items()

def mk_autoContentJetPtReweight(base):
    return varial.extensions.tex.TexContent(
        dict(get4sb(muchannel, base) + get4sb(elchannel, base)),
        include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
        name='AutoContentJetPtReweight',
    )


######################################################### AutoContentLimits ###
p_lim = os.path.join(p_postbase, 'Limits/Ind_Limits/Limit0/{0}/Limit{0}/plots')
img_lim = {
    'Limits': (
        p_lim.format('ElectronOnly')+'/limit_band_plot-acls.png',
        p_lim.format('MuonOnly')+'/limit_band_plot-acls.png',
        p_lim.format('CombinedChannels')+'/limit_band_plot-acls.png',
    ),
}

def mk_autoContentLimits(base):
    return varial.extensions.tex.TexContent(
        img_lim,
        include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
        name='AutoContentLimits',
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
                    mk_autoContentObjects(p_prebase),
                    mk_autoContentFinalSelectionHiggsVar(p_prebase),
                    mk_autoContentSelection(p_prebase),
                    mk_autoContentJetPtReweight(p_prebase),
                    mk_autoContentLimits(p_postbase)
                ]
            ),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-15-327/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)
        ])
    return tc

import time

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    # final_dir = sys.argv[2]
    all_tools = make_tex_content()
    varial.tools.Runner(all_tools, default_reuse=False)
