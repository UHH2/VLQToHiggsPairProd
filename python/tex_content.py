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
muchannel_final = 'Muon'
elchannel_final = 'Electron'

#########################################################
#=========== PRESELECTION N MINUS 1 PLOTS ===============
#=========== PRESELECTION CUTFLOW PLOTS =================
#########################################################
# p_nm1 = p_prebase + '%s/Nm1Selection/'


def get4sel(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'Nm1Selection/')
    return {
        chan+'_twoDeeCut': (
            p + 'twod_cut_hist_noIso_QCD_lin' + ext,
            p + 'twod_cut_hist_noIso_TpTp_M-1300_lin' + ext,
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
        include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
        name='AutoContentSelection',
    )

#########################################################
#=========== FINAL SELECTION CONTROL PLOTS ==============
#########################################################

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
            ('N_PrimVertices_lin', 'N_TrueInteractions_lin', 'ST_rebin_lin', 'MET_own_lin', )
        ),
    }.items()

def mk_autoContentControlPlots(base, el_channel=None, mu_channel=None):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(get4obj(muchannel, base) + get4obj(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name='AutoContentObjects',
    )


#########################################################
#=========== FINAL SELECTION HIGGS TAG PLOTS ============
#########################################################

# --TODO: implement Nm1 Plots after higgs-tags! esp. add. b-tag plots, N(higgs tags plots)
def getHiggsVar(chan, base):
    p = os.path.join(base+'/StackedAll', chan, 'PostSelection/FirstAk8SoftDropSlimmed/')
    return {
        chan+'_Nm1Var_htag': (
            p + 'Nobtag_boost_mass/n_sjbtags_medium_lin' + ext,
            p + 'Noboost_mass_1b/pt_log' + ext,
            p + 'Nomass_boost_1b/mass_sj_log' + ext,
            p + 'Nomass_boost_2b/mass_sj_log' + ext,
        ),
    }.items()

def mk_autoContentFinalSelectionHiggsVar(base, el_channel=None, mu_channel=None):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getHiggsVar(muchannel, base) + getHiggsVar(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name='AutoContentFinalSelectionHiggsVar',
    )



#########################################################
#======== FINAL SELECTION HT REWEIGHTING PLOTS ==========
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
#         include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
#         name='AutoContentJetPtReweight',
#     )

#########################################################
#========= TREEPROJECT OUTPUT NO DATA PLOTS =============
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
#         include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
#         name='AutoContentNoDataFinalRegions',
#     )

#########################################################
#====== TREEPROJECT OUTPUT SYSTEMATIC CR PLOTS ==========
#########################################################

def getSystCRPlots(chan, base):
    p = os.path.join(base, 'StackedAll/')
    # print base
    return {
        chan+'_ak4jetpt': (
            p + 'SidebandRegion_%s/pt_ld_ak4_jet_lin' % chan + ext,
            p + 'SidebandRegion_%s/pt_subld_ak4_jet_lin' % chan + ext,
            p + 'SidebandRegion_%s/pt_third_ak4_jet_lin' % chan + ext,
            p + 'SidebandRegion_%s/pt_fourth_ak4_jet_lin' % chan + ext,
        ),
        chan+'_ak8jetpt': (
            p + 'SidebandRegion_%s/pt_ld_ak8_jet_lin' % chan + ext,
            p + 'SidebandRegion_%s/pt_subld_ak8_jet_lin' % chan + ext,
        ),
        chan+'_eventvar': (
            p + 'SidebandRegion_%s/ST_rebin_flex_lin' % chan + ext,
            p + 'SidebandRegion_%s/HT_rebin_flex_lin' % chan + ext,
            p + 'SidebandRegion_%s/primary_lepton_pt_lin' % chan + ext,
            p + 'SidebandRegion_%s/met_lin' % chan + ext,
        ),
        chan+'_njets': (
            p + 'SidebandRegion_%s/n_ak4_lin' % chan + ext,
            p + 'SidebandRegion_%s/n_ak8_lin' % chan + ext,
        )
    }.items()

def mk_autoContentSystematicCRPlots(base, el_channel=None, mu_channel=None, name='AutoContentSystematicCRPlots'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getSystCRPlots(muchannel, base) + getSystCRPlots(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name=name,
    )

#########################################################
#========= TREEPROJECT OUTPUT N MINUS 1 PLOTS ===========
#########################################################

def getFinalVar(chan, base):
    p = os.path.join(base, 'StackedAll/')
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

def mk_autoContentSignalControlRegion(base, el_channel=None, mu_channel=None, name='AutoContentSignalControlRegion'):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    return varial.extensions.tex.TexContent(
        dict(getFinalVar(muchannel, base) + getFinalVar(elchannel, base)),
        include_str=r'\includegraphics[width=0.45\textwidth]{%s}',
        name=name,
    )


#########################################################
#============= TREEPROJECT OUTPUT LIMITS ================
#=========== TREEPROJECT OUTPUT SYSTEMATICS =============
#########################################################

def getLimPlotsAll(base):
    # p_lim = os.path.join(base, 'LimitsSyst/Ind_Limits/Limit0/{0}/Limit{0}')
    return {
        'Limits': (
            os.path.join(base, 'LimitsAllUncertsAllRegions/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
            os.path.join(base, 'LimitsAllUncertsOnlyEl/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
            os.path.join(base, 'LimitsAllUncertsOnlyMu/Ind_Limits/Limit0/LimitsWithGraphs/LimitCurvesCompared/tH100tZ0bW0_log' + ext),
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

def my_mod(table):
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
        + find_column_string(lines[1], 'el trg+id') + find_column_string(lines[1], 'mu trg+id')
    for i, line in enumerate(lines):
        lines[i] = remove_column(line, indizes)
    table = '\n'.join(lines)
    return table


def getSysTab(chan, base, mod=my_mod):
    p_lim = os.path.join(base, 'LimitsSyst/Ind_Limits/Limit0/{0}/Limit{0}')
    new_files = []
    if mod:
        for filename in list(p_lim.format('CombinedChannels')+'/sysrate_tables_{0}_{1}.tex'.format(g, chan)\
                    for g in ['SidebandRegion', 'SignalRegion1b', 'SignalRegion2b']):
            # print filename
            with open(filename) as f:
                cont = f.read()
            with open(filename.replace('.tex', '_mod.tex'), 'w') as f:
                # print mod(cont)
                f.write(mod(cont))
            new_files.append(filename.replace('.tex', '_mod.tex'))

    return {
        chan+'_side_sys_tab.tex':
            new_files[0],
        chan+'_sig1b_sys_tab.tex':
            new_files[1],
        chan+'_sig2b_tab.tex':
            new_files[2],
    }.items()

def mk_autoContentLimits(base, el_channel=None, mu_channel=None, name='AutoContentLimits', prefix=''):
    muchannel = mu_channel or mu_channel_def
    elchannel = el_channel or el_channel_def
    tmp_dict = getLimPlotsSingle(base, prefix) if prefix else getLimPlots(base)
    return varial.extensions.tex.TexContent(
        tmp_dict,
        # dict(getSysTab(muchannel, base) + getSysTab(elchannel, base)),
        include_str=r'\includegraphics[width=0.49\textwidth]{%s}',
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
                    mk_autoContentLimits(p_postbase)
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
