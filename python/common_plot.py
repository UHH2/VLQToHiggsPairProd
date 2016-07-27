import os
import copy
import pprint
import cPickle

import varial.analysis
import varial.generators as gen
import varial.rendering as rnd

import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.operations as op
import varial.wrappers
import varial.util as util

from ROOT import THStack, TH2, TLatex

lumi_times_pure_BR = 2630.*0.111
lumi_times_mixed_BR = 2630.*0.222
lumi = 2630.
lumi_ele = 2540.

normfactors = {
    # 'TpTp' : 20.,
    # '_thX' : 1./0.56,
    # '_other' : 1./0.44,
    # '_thth' : 1./0.111,
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
    'BpBp_M-0700' : 1./0.455,
    'BpBp_M-0800' : 1./0.196,
    'BpBp_M-0900' : 1./0.0903,
    'BpBp_M-1000' : 1./0.0440,
    'BpBp_M-1100' : 1./0.0224,
    'BpBp_M-1200' : 1./0.0118,
    'BpBp_M-1300' : 1./0.00639,
    'BpBp_M-1400' : 1./0.00354,
    'BpBp_M-1500' : 1./0.00200,
    'BpBp_M-1600' : 1./0.001148,
    'BpBp_M-1700' : 1./0.000666,
    'BpBp_M-1800' : 1./0.000391,
}

normfactors_wrong = {
    # 'TpTp' : 20.,
    # '_thX' : 1./0.56,
    # '_other' : 1./0.44,
    'TpTp_M-0700' : (1./0.455)*(1748747./1769230.),
    'TpTp_M-0800' : (1./0.196)*(4145693./4021428.),
    'TpTp_M-0900' : (1./0.0903)*(9189878./9196013.),
    'TpTp_M-1000' : (1./0.0440)*(18700000./18604545.),
    'TpTp_M-1100' : (1./0.0224)*(36678571./36107142.),
    'TpTp_M-1200' : (1./0.0118)*(70576271./69305084.),
    'TpTp_M-1300' : (1./0.00639)*(129953051./129577464.),
    'TpTp_M-1400' : (1./0.00354)*(235254237./233559322.),
    'TpTp_M-1500' : (1./0.00200)*(406100000./416000000.),
    'TpTp_M-1600' : (1./0.001148)*(804000000./704878048.),
    'TpTp_M-1700' : (1./0.000666)*(1664800000./1194594594.),
    'TpTp_M-1800' : (1./0.000391)*(3331200000./2112020460.),
}

norm_reg_dict = {
    'Baseline' : 5,
    'BaseLineSelection' : 5,
    'SidebandRegion' : 5,
    'SidebandTTJetsRegion' : 5,
    'SidebandWPlusJetsRegion' : 5,
    'SignalRegion1b' : 5,
    'SignalRegion2b' : 1,
}

def get_style():
    if varial.settings.style == 'PAS':
        return [varial.rendering.BottomPlotRatioSplitErr,
            varial.rendering.Legend,
            varial.rendering.TextBox(textbox=TLatex(0.23, 0.89, "#scale[0.8]{#bf{CMS}} #scale[0.7]{#it{Preliminary}}")),
            varial.rendering.TextBox(textbox=TLatex(0.65, 0.89, "#scale[0.6]{2.7 fb^{-1} (13 TeV)}")),
            ]
    else:
        return [varial.rendering.BottomPlotRatioSplitErr,
            varial.rendering.Legend,
            varial.rendering.TextBox(textbox=TLatex(0.65, 0.89, "#scale[0.6]{2.7 fb^{-1} (13 TeV)}")),
            ]

mod_dict = {

    'twod_cut_hist_noIso_px' : {
            'y_max_log_fct' : 10.,
            'y_min_gr_zero' : 10,
            },
    'twod_cut_hist_noIso_py' : {
            'y_max_log_fct' : 100.,
            'y_min_gr_zero' : 0.1,
            },

    ##### GEN VARIABLES ######
    'higgs_to_bb_pt_all_lin' : {
            'title' : 'p_{T}(Higgs) [GeV]',
            'y_max_fct' : 1.2,
            },
    'higgs_to_bb_dRDecay_all_lin' : {
            'title' : '#Delta R(b, b)_{Higgs}',
            'y_max_fct' : 1.2,
            },
    'tprime_pt_all' : {
            'title' : 'p_{T}(T quark) [GeV]',
            'y_max_fct' : 1.2,
            },
    'tprime_dRDecay_all' : {
            'title' : '#Delta R(t, H)_{T quark}',
            'y_max_fct' : 1.2,
            },

    ##### GENERAL VARIABLES ######
    'ST' : {
            'rebin' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            },
    'ST_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 2e-3,
            },
    'HT' : {
            'rebin' : [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            },
    'HT_rebin_flex' : {
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 2e-3,
            },
    'primary_electron_pt' : {
            'rebin' : 25,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'title' : 'Primary Electron p_{T} [GeV]',
            },
    'primary_muon_pt' : {
            'rebin' : 25,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'title' : 'Primary Muon p_{T} [GeV]',
            },
    'primary_lepton_pt' : {
            'rebin' : 25,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'title' : 'Primary Lepton p_{T} [GeV]',
            },
    'met' : {
            'rebin' : 30,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'pt_ld_ak4_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (1st AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'jets[].m_pt' : {
            'rebin' : 30,
            # 'title' : 'p_{T} (1st AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'pt_subld_ak4_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (2nd AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'pt_third_ak4_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (3rd AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'pt_fourth_ak4_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (4th AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'jets[2].m_pt' : {
            'rebin' : 30,
            'title' : 'p_{T} (3rd AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'jets[3].m_pt' : {
            'rebin' : 30,
            'title' : 'p_{T} (4th AK4 Jet) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            'y_max_fct' : 1.5,
            },
    'pt_ld_ak8_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (1st AK8 Jet) [GeV]',
            'y_max_fct' : 1.5,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            },
    'pt_subld_ak8_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} (2nd AK8 Jet) [GeV]',
            'y_max_fct' : 1.5,
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 0.1,
            },
    'n_ak4' : {
            'title' : 'N(AK4 jets)',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 2e-2,
            },
    'n_ak8' : {
            'title' : 'N(AK8 jets)',
            'y_max_log_fct' : 1000000.,
            'y_min_gr_zero' : 2e-3,
            },
    'ak4_jets_btagged_dR_higgs_tags_1b_med' : {
            # 'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 2e-1,
            'set_leg_2_col_lin' : True
            },

    ##### HIGGS TAG VARIABLES ######
    'mass_sj' : {
            'rebin' : 30,
            'title' : 'M_{soft-drop}(Higgs tag) [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            },
    'n_sjbtags_medium' : {
            'title' : 'N(subjet b tags)',
            'y_max_log_fct' : 1000.,
            },
    # 'pt' : {
    #         'rebin' : 30,
    #         'title' : 'p_{T} leading Higgs tag [GeV]',
    #         'y_max_log_fct' : 1000.,
    #         'y_max_fct' : 1.5,
    #         },
    'nomass_boost_1b_mass' : {
            'rebin' : 30,
            'title' : 'M_{soft-drop}(Higgs tag, 1 subjet b-tag) [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            },
    'nomass_boost_2b_mass' : {
            'rebin' : 15,
            'title' : 'M_{soft-drop}(Higgs tag, 2 subjet b-tags) [GeV]',
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.2
            },
    'nobtag_boost_mass_nsjbtags' : {
            'title' : 'N(subjet b tags)',
            'y_min_gr_zero' : 10,
            },
    'noboost_mass_1b_pt' : {
            'title' : 'p_{T}(Higgs tag, 1 subjet b-tag) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 1e-3,
            'scale' : 0.2
            },
    'noboost_mass_2b_pt' : {
            'title' : 'p_{T}(Higgs tag, 2 subjet b-tags) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 1e-3,
            'scale' : 0.2
            },
    'noboost_mass_1b[0].m_pt' : {
            'title' : 'p_{T}(Higgs tag, 1 subjet b-tag) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 1e-3,
            'scale' : 0.2
            },
    'noboost_mass_2b[0].m_pt' : {
            'title' : 'p_{T}(Higgs tag, 2 subjet b-tags) [GeV]',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 1e-3,
            'scale' : 0.2
            },

    ##### FINAL CATEGORY VARIABLES ######
    'n_additional_btags_medium' : {
            'title' : 'N(AK4 b tags)',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 1e-3,
            'set_leg_2_col_log' : True
            },
    'n_higgs_tags_1b_med' : {
            'title' : 'N(Higgs tag, 1 subjet b-tag)',
            'y_max_log_fct' : 1000.,
            'y_min_gr_zero' : 3e-3,
            # 'set_leg_2_col_log' : True
            },
    'n_higgs_tags_2b_med' : {
            'y_max_log_fct' : 1000.,
            'title' : 'N(Higgs tag, 2 subjet b-tags)',
            'y_min_gr_zero' : 1e-3,
            # 'set_leg_2_col_log' : True
            },

}





signal_indicators = ['TpTp_', 'BpBp_']

#====SELECT_FILES FUNCTIONS====

def file_select(datasets_to_plot, src=''):
    if src:
        src_dir = src
    else:
        src_dir = varial.analysis.cwd+src_dir_rel

    file_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root') and '.sframe' not in f
            and any(g in f for g in datasets_to_plot)
        )]
    return file_list

    

#====GENERAL FUNCTIONS====

def merge_finalstates_channels(wrps, finalstates=(), suffix='', print_warning=True):
    """histos must be sorted!!"""

    @varial.history.track_history
    def merge_decay_channel(w):
        return w

    def do_merging(buf):
        res = varial.operations.merge(buf)
        res.sample = res.sample+suffix
        res.legend = res.legend+suffix
        # res.in_file_path = buf[0].in_file_path[1:]
        del buf[:]
        return merge_decay_channel(res)

    buf = []
    for w in wrps:
        if any(w.finalstate == p for p in finalstates):
            buf.append(w)
            if len(buf) == len(finalstates):
                yield do_merging(buf)
        else:
            if buf:
                if print_warning:
                    print 'WARNING In merge_decay_channels: buffer not empty.\n' \
                          'finalstates:\n' + str(finalstates) + '\n' \
                          'Flushing remaining items:\n' + '\n'.join(
                        '%s, %s' % (w.sample, w.in_file_path) for w in buf
                    )
                yield do_merging(buf)
            yield w
    if buf:
        yield do_merging(buf)


def norm_smpl(wrps, smpl_fct=None, norm_all=1., calc_scl_fct=True):
    for w in wrps:
        if smpl_fct:
            for fct_key, fct_val in smpl_fct.iteritems():
                if fct_key in w.sample:
                    # if w.analyzer = 'NoSelection' or
                    if calc_scl_fct:
                        if hasattr(w, 'scl_fct'):
                            w.scl_fct *= fct_val
                        else:
                            op.add_wrp_info(w, scl_fct=lambda _: fct_val)
                    w.histo.Scale(fct_val)
        if hasattr(w, 'scl_fct'):
            w.scl_fct *= norm_all
        else:
            op.add_wrp_info(w, scl_fct=lambda _: norm_all)
        w.histo.Scale(norm_all)
        yield w

def norm_to_int(wrps, use_bin_width=False):
    option = "width" if use_bin_width else ""
    for w in wrps:
        integr = w.histo.Integral(option)
        w.histo.Scale(1./integr)
        if not w.is_signal and not w.is_data:
            w.sample = "Background"
            w.legend = "Background"
        yield w

# @history.track_history
def scale_signal(wrp, fct=1.):
    if not hasattr(wrp, 'is_scaled'):
        if fct >= 5:
            fct = int(fct)
            if fct % 5 > 2:
                fct += (5 - fct % 5)
            else: fct -= fct % 5
        elif fct >= 1.:
            fct = int(fct)
        elif fct >= 0.2:
            fct = 1
        else:
            fct *= 5
        if hasattr(wrp, 'scl_fct'):
            wrp.scl_fct *= fct
        else:
            op.add_wrp_info(wrp, scl_fct=lambda _: fct)
        wrp.histo.Scale(fct)
        op.add_wrp_info(wrp, is_scaled=lambda w: True)
        if fct >= 1:
            wrp.legend +=' (%.2g pb)' % fct
        elif fct < 1:
            wrp.legend +=' (%.1g pb)' % fct
    # else:
    #     print 'WARNING! histogram '+wrp.in_file_path+' already scaled'

def norm_to_bkg(grps):
    for g in grps:
        bkg = g.wrps[0]
        if not (bkg.is_signal or bkg.is_data):
            max_bkg = bkg.histo.GetMaximum()
            max_sig = 0.
            for w in g.wrps:
                if w.is_signal:
                    if not max_sig:
                        max_sig = w.histo.GetMaximum()
                        fct_val = (max_bkg/max_sig)*0.2
                    scale_signal(w, fct_val)            
        yield g


def norm_stack_to_integral(grps):
    for g in grps:
        for w in g:
            # bkg = g.wrps[0]
            integr_nom = w.histo.Integral() or 1.
            w.histo.Scale(1./integr_nom)
            if isinstance(w, varial.wrappers.StackWrapper):
                new_stk = THStack(w.name, w.title)
                new_stk.Add(w.histo)
                w.stack = new_stk
                w.legend = 'Background'
                w.sample = 'Background'
                # for h in w.stack.GetHists():
                #     h.Scale(1./integr_nom)
            if w.histo_sys_err:
                integr_err = w.histo_sys_err.Integral() or 1.
                w.histo_sys_err.Scale(1./integr_err)
        yield g

def norm_to_fix_xsec(wrps):
    for w in wrps:
        if w.is_signal:
            base_fct = 20.
            for r, f in norm_reg_dict.iteritems():
                if r in w.in_file_path:
                    base_fct = f
            mod_wrp_dict = mod_dict.get(w.name, None)
            if mod_wrp_dict:
                mult_fct = mod_wrp_dict.get('scale', None)
                if mult_fct:
                    base_fct *= mult_fct
            scale_signal(w, base_fct)            
        yield w


def mod_legend(wrps):
    for w in wrps:
        if w.legend.startswith('MC_'):
            w.legend = w.legend[3:]
        if w.is_data:
            w.legend = 'data'
        if w.legend.startswith('TpTp'):
            suf = w.legend[11:]
            mass = float(w.legend[7:11])/1000.
            w.legend = 'T#bar{T} (%.1f TeV)' % mass
            w.legend += suf
        if w.legend == 'TTbar':
            w.legend = 't#bar{t}'
        if w.legend == 'WJets':
            w.legend = 'W + jets'
        if w.legend == 'DYJetsToLL' or w.legend == 'DYJets':
            w.legend = 'DY + jets'
        if w.legend == 'SingleTop':
            w.legend = 'Single t'
        yield w

def mod_legend_eff_counts(wrps):
    for w in wrps:
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5] + '#rightarrow tH#bar{t}H'
        if w.legend.endswith('_thtz'):
            w.legend = w.legend[:-5] + '#rightarrow tH#bar{t}Z'
        if w.legend.endswith('_thbw'):
            w.legend = w.legend[:-5] + '#rightarrow tH#bar{b}W'
        if w.legend.endswith('_tztz'):
            w.legend = w.legend[:-9] + '#rightarrow tZ#bar{t}Z'
        if w.legend.endswith('_tzbw'):
            w.legend = w.legend[:-9] + '#rightarrow tZ#bar{b}W'
        if w.legend.endswith('_bwbw'):
            w.legend = w.legend[:-9] + '#rightarrow bW#bar{b}W'
        if w.legend.endswith('_thX'):
            w.legend = w.legend[:-4] + '#rightarrow tH+X'
        if w.legend.endswith('_other'):
            w.legend = w.legend[:-6] + '#rightarrow other'
        if w.legend.endswith('_incl'):
            w.legend = w.legend[:-5] + '#rightarrow incl.'
        yield w

def mod_legend_no_thth(wrps):
    if varial.settings.style != 'AN':
        arr = '#rightarrow tHtH'
    else:
        arr = ''
    for w in wrps:
        if w.legend.endswith('_thth') or w.legend.endswith(' tHtH'):
            w.legend = w.legend[:-5] + arr
        yield w

def mod_title(wrps):
    for w in wrps:
        mod_wrp_dict = mod_dict.get(w.name, None)
        if mod_wrp_dict:
            new_title = mod_wrp_dict.get('title', None)
            if new_title:
                w.histo.GetXaxis().SetTitle(new_title)
        if 'topjet' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('topjet', 'AK8 jet'))
        if 'p_T' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('p_T', 'p_{T}'))
        if 'ST' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('ST', 'S_{T}'))
        if 'HT' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('HT', 'H_{T}'))
        if 'Pt' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('Pt', 'p_{T}'))
        if 'MET' in w.histo.GetXaxis().GetTitle():
            title = w.histo.GetXaxis().GetTitle()
            w.histo.GetXaxis().SetTitle(title.replace('MET', 'missing E_{T}'))
        yield w



def add_wrp_info(wrps, sig_ind=None):
    def fix_get_samplename(wrp):
        fname = os.path.basename(wrp.file_path)
        if fname.startswith('uhh2'):
            smpl = fname.split('.')[-2]
            if smpl == 'TTbar_split' or smpl == 'TTbar_incl':
                smpl = 'TTbar'
            return smpl
        else:
            smpl = os.path.splitext(fname)[0]
            if smpl == 'TTbar_split' or smpl == 'TTbar_incl':
                smpl = 'TTbar'
            return smpl

    def fix_ttbar_smpl(wrp):
        if 'jug_file' in wrp.file_path:
            smpl = os.path.splitext(wrp.file_path)[0]
            smpl = os.path.basename(smpl)
            smpl = '-'.join(smpl.split('-')[3:])
        else:
            smpl = vlq_common.get_samplename(wrp)
        if smpl == 'TTbar_split' or smpl == 'TTbar_incl':
            smpl = 'TTbar'
        return smpl


    def batch_tp_infilepath(wrp):
        filename = os.path.basename(wrp.file_path)
        filename = filename.split('.')[0]
        cat = filename.split('-')[2]
        return cat+'/'+'-'.join(filename.split('-')[3:])

    sig_ind = sig_ind or signal_indicators
    if varial.settings.fix_presel_sample:
        get_samplename = fix_get_samplename
    else:
        get_samplename = fix_ttbar_smpl
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=get_samplename,
        legend=get_samplename,
        # in_file_path=lambda w: w.in_file_path if 'jug-file' not in w.file_path else batch_tp_infilepath,
        is_signal=lambda w: any(s in w.file_path for s in sig_ind),
        is_data=lambda w: 'Run20' in w.file_path,
        variable=lambda w: w.in_file_path.split('/')[-1],
        sys_info=vlq_common.get_sys_info,
    )


def add_sample_integrals(canvas_builders):
    """
    Adds {'legend1' : histo_integral, ...} to canvases.
    """
    def integral_histo_wrp(wrp):
        fct = 1.
        if hasattr(wrp, 'scl_fct'):
            fct = wrp.scl_fct
        nom_sum = util.integral_and_error(wrp.histo)
        if len(nom_sum) == 2:
            nom_sum = (nom_sum[0]/fct, nom_sum[1]/fct)
        sys_sum = (op.get_sys_int(wrp)
                   if wrp.histo_sys_err
                   else tuple())
        if len(sys_sum) == 2:
            sys_sum = (sys_sum[0]/fct, sys_sum[1]/fct)
        return [(wrp.sample, nom_sum + sys_sum)]

    def integral_stack_wrp(wrp):
        for hist in wrp.obj.GetHists():
            fct = 1.
            if hasattr(wrp, 'scl_fct'):
                fct = wrp.scl_fct
            sum_tmp = util.integral_and_error(hist)
            sys_tmp = getattr(wrp, hist.GetTitle()+'__sys', (sum_tmp[0], 0.))
            if len(sum_tmp) == 2:
                sum_tmp = (sum_tmp[0]/fct, sum_tmp[1]/fct, sys_tmp[0]/fct, sys_tmp[1]/fct)
            yield hist.GetTitle(), sum_tmp
        nom_sum = util.integral_and_error(wrp.histo)
        # if len(nom_sum) == 2:
            # nom_sum = (nom_sum[0]*2, nom_sum[1]*2)
        sys_sum = (op.get_sys_int(wrp)
                   if wrp.histo_sys_err
                   else tuple())
        # if len(sys_sum) == 2:
            # sys_sum = (sys_sum[0]*2, sys_sum[1]*2)
        yield 'bkg_sum', nom_sum + sys_sum

    def integral(wrp):
        if isinstance(wrp, rnd.StackRenderer):
            return integral_stack_wrp(wrp)
        else:
            return integral_histo_wrp(wrp)

    for cnv in canvas_builders:
        # TODO when rendering goes generator
        cnv.renderers[0].__dict__.update(dict(
            ('Integral___' + sample, integ)
            for r in cnv.renderers
            if isinstance(r, rnd.HistoRenderer)  # applies also to StackRnd.
            for sample, integ in integral(r)
        ))
        yield cnv

# def add_sample_integrals(canvas_builders):
#     """
#     Adds {'legend1' : histo_integral, ...} to canvases.
#     """
#     def integral_histo_wrp(wrp):
#         fct = 1.
#         if hasattr(wrp, 'scl_fct'):
#             fct = wrp.scl_fct
#         return [(wrp.legend, wrp.obj.Integral()/fct)]

#     def integral_stack_wrp(wrp):
#         for hist in wrp.obj.GetHists():
#             fct = 1.
#             if hasattr(wrp, 'scl_fct'):
#                 fct = wrp.scl_fct
#             yield hist.GetTitle(), hist.Integral()/fct

#     def integral(wrp):
#         if isinstance(wrp, rnd.StackRenderer):
#             return integral_stack_wrp(wrp)
#         else:
#             return integral_histo_wrp(wrp)

#     for cnv in canvas_builders:
#         # TODO when rendering goes generator
#         cnv.renderers[0].__dict__.update(dict(
#             ('Integral__' + legend, integ)
#             for r in cnv.renderers
#             if isinstance(r, rnd.HistoRenderer)  # applies also to StackRnd.
#             for legend, integ in integral(r)
#         ))
#         yield cnv



def rebin_st_and_nak4(wrps):
    # st_bounds = [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.]
    # ht_bounds = [0., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.]
    # subl_jet_pt_bounds = range(0, 600, 100) + [700, 1000, 1500]
    # foll_jet_pt_bounds = range(0, 200, 33) + [300, 400, 1000]
    # nak4_bounds = list(x - 0.5 for x in xrange(0, 7))+[13.5]
    for w in wrps:
        if not isinstance(w.histo, TH2):
            mod_wrp_dict = mod_dict.get(w.name, None)
            rebin_ind = False
            if mod_wrp_dict:
                rebin_fct = mod_wrp_dict.get('rebin', None)
                if (isinstance(rebin_fct, list)):
                    new_w_flex = op.rebin(w, rebin_fct, True)
                    new_w_flex.name = w.name+'_rebin_flex'
                    new_w_flex.in_file_path = w.in_file_path.replace(w.name, w.name+'_rebin_flex')
                    yield new_w_flex
                elif (isinstance(rebin_fct, int)):
                    w = op.rebin_nbins_max(w, rebin_fct)
                    rebin_ind = True
            # if not rebin_ind:
            #     w = op.rebin_nbins_max(w, 60)
        yield w

# def leg_2_col(rnd, dict_leg=varial.settings.defaults_Legend):
#     if varial.settings.style != 'AN':
#         dict_leg.update({'n_col' : 2})
#         leg_mod(rnd, dict_leg)

def leg_mod(rnd, dict_leg=varial.settings.defaults_Legend, n_col=1):
    # if varial.settings.style != 'AN':
    rnd.legend.SetNColumns(n_col)
    rnd.legend.SetTextSize(dict_leg.get('box_text_size', varial.settings.box_text_size))
    n_entries = len(rnd.legend.GetListOfPrimitives())
    x_pos   = dict_leg['x_pos']
    y_pos   = dict_leg['y_pos']
    width   = dict_leg['label_width']
    height  = dict_leg['label_height'] * n_entries / float(n_col)
    if n_col ==  2:
        rnd.legend.SetX1(x_pos - 3*width/2.)
        rnd.legend.SetY1(y_pos - 0.1*height)
        rnd.legend.SetX2(x_pos + width/2.)
        rnd.legend.SetY2(y_pos + 0.9*height)
    else:
        rnd.legend.SetX1(x_pos - width/2.)
        rnd.legend.SetY1(y_pos - height/2.)
        rnd.legend.SetX2(x_pos + width/2.)
        rnd.legend.SetY2(y_pos + height/2.)

default_canv_attr = {
    'y_min_gr_zero' : 1e-9,
    'y_max_fct' : 1.,
    'y_max_log_fct' : 1.,
    'set_leg_2_col_lin' : False,
    'set_leg_2_col_log' : False,
    'set_leg_1_col_lin' : False,
    'set_leg_1_col_log' : False,
}

# def mod_post_canv_new(grps):
#     for g in grps:
#         g.renderers[0].name += '_'+g.renderers[0].scale
#         _, y_max = g.y_bounds
#         canv_attr = dict(default_canv_attr)
#         mod_wrp_dict = mod_dict.get(g.name, None)
#         if not any(w.is_data for w in g.renderers):
#             g.canvas.SetCanvasSize(varial.settings.canvas_size_x, int(16./19.*varial.settings.canvas_size_y))
#         if mod_wrp_dict:
#             canv_attr.update(mod_wrp_dict)
#         if g.renderers[0].scale == 'lin':
#             g.first_drawn.SetMaximum(y_max * canv_attr['y_max_fct'])
#             if canv_attr['set_leg_2_col_lin']:
#                 if isinstance(canv_attr['set_leg_2_col_lin'], dict):
#                     leg_mod(g, canv_attr['set_leg_2_col_lin'], n_col=2)
#                 else:
#                     leg_mod(g, n_col=2)
#             if canv_attr['set_leg_1_col_lin']:
#                 if isinstance(canv_attr['set_leg_1_col_lin'], dict):
#                     leg_mod(g, canv_attr['set_leg_1_col_lin'])
#                 else:
#                     leg_mod(g)
#         elif g.renderers[0].scale == 'log':
#             if isinstance(g.first_drawn, TH2):
#                 g.main_pad.SetLogz(1)
#             else:
#                 g.main_pad.SetLogy(1)
#             g.first_drawn.SetMinimum(canv_attr['y_min_gr_zero'])
#             g.first_drawn.SetMaximum(y_max * canv_attr['y_max_log_fct'])
#             if canv_attr['set_leg_2_col_log']:
#                 if isinstance(canv_attr['set_leg_2_col_log'], dict):
#                     leg_mod(g, canv_attr['set_leg_2_col_log'], n_col=2)
#                 else:
#                     leg_mod(g, n_col=2)
#             if canv_attr['set_leg_1_col_log']:
#                 if isinstance(canv_attr['set_leg_1_col_log'], dict):
#                     leg_mod(g, canv_attr['set_leg_1_col_log'])
#                 else:
#                     leg_mod(g)
#         yield g


def mod_post_canv(grps):
    for g in grps:
        if not any(w.is_data for w in g.renderers):
            g.canvas.SetCanvasSize(varial.settings.canvas_size_x, int(16./19.*varial.settings.canvas_size_y))
        y_min, y_max = g.y_bounds
        canv_attr = dict(default_canv_attr)
        mod_wrp_dict = mod_dict.get(g.name, None)
        if mod_wrp_dict:
            canv_attr.update(mod_wrp_dict)
        if y_max > 1.:
            g.first_drawn.SetMinimum(canv_attr['y_min_gr_zero'])
            g.y_min_gr_zero = canv_attr['y_min_gr_zero']
        if g.renderers[0].scale == 'lin':
            g.first_drawn.SetMaximum(y_max * canv_attr['y_max_fct'])
            if canv_attr['set_leg_2_col_lin']:
                if isinstance(canv_attr['set_leg_2_col_lin'], dict):
                    leg_mod(g, canv_attr['set_leg_2_col_lin'], n_col=2)
                else:
                    leg_mod(g, n_col=2)
            if canv_attr['set_leg_1_col_lin']:
                if isinstance(canv_attr['set_leg_1_col_lin'], dict):
                    leg_mod(g, canv_attr['set_leg_1_col_lin'])
                else:
                    leg_mod(g)
        elif g.renderers[0].scale == 'log':
            g.renderers[0].name += '_leg'
            g.first_drawn.SetMaximum(y_max * canv_attr['y_max_log_fct'])
            if canv_attr['set_leg_2_col_log']:
                if isinstance(canv_attr['set_leg_2_col_log'], dict):
                    leg_mod(g, canv_attr['set_leg_2_col_log'], n_col=2)
                else:
                    leg_mod(g, n_col=2)
            if canv_attr['set_leg_1_col_log']:
                if isinstance(canv_attr['set_leg_1_col_log'], dict):
                    leg_mod(g, canv_attr['set_leg_1_col_log'])
                else:
                    leg_mod(g)
        yield g


def copy_wrp_for_log(wrps):
    for w in wrps:
        w = op.add_wrp_info(w, scale=lambda _: 'lin')
        mod_wrp_dict = mod_dict.get(w.name, None)
        if mod_wrp_dict:
            copy_for_log = mod_wrp_dict.get('y_max_log_fct', 1.) != 1.
            if copy_for_log:
                new_w = op.copy(w)
                new_w = op.add_wrp_info(new_w, scale=lambda _: 'log')
                yield new_w
        yield w

def ini_def_leg(grps):
    for g in grps:
        g.legend.SetNColumns(1)
        # if g.name == 'mass_sj':
        n_entries = len(g.legend.GetListOfPrimitives())
        x_pos   = varial.settings.defaults_Legend['x_pos']
        y_pos   = varial.settings.defaults_Legend['y_pos']
        width   = varial.settings.defaults_Legend['label_width']
        height  = varial.settings.defaults_Legend['label_height'] * n_entries
        g.legend.SetX1(x_pos - width/2.)
        g.legend.SetY1(y_pos - height/2.)
        g.legend.SetX2(x_pos + width/2.)
        g.legend.SetY2(y_pos + height/2.)
        yield g

def mod_shift_leg(grps):
    for g in grps:
        # if g.name == 'mass_sj':
        n_entries = len(g.legend.GetListOfPrimitives())
        x_pos   = 0.7
        y_pos   = 0.72
        width   = 0.33
        height  = 0.035 * n_entries
        g.legend.SetX1(x_pos - width/2.)
        g.legend.SetY1(y_pos - height/2.)
        g.legend.SetX2(x_pos + width/2.)
        g.legend.SetY2(y_pos + height/2.)
        yield g

def mod_no_2D_leg(grps):
    for g in grps:
        g.legend.SetNColumns(1)
        # if g.name == 'mass_sj':
        n_entries = len(g.legend.GetListOfPrimitives())
        x_pos   = 0.7
        y_pos   = 0.72
        width   = 0.33
        height  = 0.035 * n_entries
        g.legend.SetX1(x_pos - width/2.)
        g.legend.SetY1(y_pos - height/2.)
        g.legend.SetX2(x_pos + width/2.)
        g.legend.SetY2(y_pos + height/2.)
        yield g

class BottomPlotUncertRatio(varial.rendering.BottomPlot):
    """Same as BottomPlotRatio, but split MC and data uncertainties."""

    def check_renderers(self):
        n_hists = len(self.renderers)

        # if 'TH2' in self.renderers[0].type:
        #     return False

        if n_hists != 3:
            print self.renderers
            raise RuntimeError('ERROR BottomPlotControlSignalRatio can only be created '
                               'with exactly three histograms!')
        return n_hists == 3

    def define_bottom_hist(self):
        def plus_minus_key(w):
            if w.sys_info.endswith('__plus'):
                return 2
            elif w.sys_info.endswith('__minus'):
                return 1
            else:
                return 0

        rnds = self.renderers
        rnds = sorted(rnds, key=plus_minus_key) 
        nom_histo = rnds[0].histo.Clone()
        div_hist_down = rnds[1].histo.Clone()
        div_hist_up = rnds[2].histo.Clone()
        div_hist_down.Add(nom_histo, -1)
        div_hist_up.Add(nom_histo, -1)
        div_hist_down.Divide(nom_histo)
        div_hist_up.Divide(nom_histo)
        for i in xrange(1, nom_histo.GetNbinsX() + 1):
            if nom_histo.GetBinContent(i) == 0. and\
             div_hist_up.GetBinContent(i) == 0. and\
             div_hist_down.GetBinContent(i) == 0.:
                nom_histo.SetBinError(i, 0.) 
                div_hist_down.SetBinContent(i, 0.)
                div_hist_up.SetBinContent(i, 0.)
            if nom_histo.GetBinContent(i):
                nom_histo.SetBinError(i, nom_histo.GetBinError(i)/nom_histo.GetBinContent(i)) 
            nom_histo.SetBinContent(i, 0.) 
            div_hist_down.SetBinError(i, 0.)
            div_hist_up.SetBinError(i, 0.)
        div_hist_down.SetYTitle('#frac{uncert. hist - nominal hist}{nominal hist}')
        div_hist_up.SetYTitle('#frac{uncert. hist - nominal hist}{nominal hist}')
        nom_histo.SetYTitle('#frac{uncert. hist - nominal hist}{nominal hist}')
        varial.settings.stat_error_style(nom_histo)
        div_hist_up.SetLineColor(varial.settings.colors['plus'])
        div_hist_down.SetLineColor(varial.settings.colors['minus'])
        if abs(div_hist_up.GetMaximum()) > abs(div_hist_down.GetMinimum()):
            self.bottom_hist = div_hist_up
            self.bottom_hist_sec = div_hist_down
        else:
            self.bottom_hist = div_hist_down
            self.bottom_hist_sec = div_hist_up
        self.bottom_hist_mc_err = nom_histo


    def draw_full_plot(self):
        """Draw mc error histo below data ratio."""
        super(BottomPlotUncertRatio, self).draw_full_plot()
        if not self.dec_par['renderers_check_ok']:
            return
        self.second_pad.cd()
        n_bins = self.bottom_hist.GetNbinsX()
        mini = min(self.bottom_hist.GetBinContent(i+1) for i in xrange(n_bins))
        maxi = max(self.bottom_hist.GetBinContent(i+1) for i in xrange(n_bins))
        y_range = max(abs(mini), abs(maxi))
        y_range = min(y_range, 2.)
        y_range += .1*y_range
        y_min, y_max = -y_range, y_range
        self.bottom_hist.GetYaxis().SetRangeUser(y_min, y_max)
        self.bottom_hist.GetYaxis().SetNoExponent()
        self.bottom_hist.SetMarkerSize(0)
        self.bottom_hist.GetYaxis().SetTitleSize(0.10)
        self.bottom_hist_sec.SetMarkerSize(0)
        self.bottom_hist.Draw('E0')
        self.bottom_hist_sec.Draw('sameE0')
        self.bottom_hist_mc_err.Draw('sameE2')
        self.main_pad.cd()


def get_dict(hist_path, var):
    def tmp(base_path):
        path = hist_path
        if not os.path.exists(path):
            path = os.path.join(base_path, path)
        with open(os.path.join(path, '_varial_infodata.pkl')) as f:
            res = cPickle.load(f)
        return res[var]
    return tmp

table_block_signal = [
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0700_thth' in w, True),
    (r'T#bar{T} (0.9 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0900_thth' in w, True),
    (r'T#bar{T} (1.1 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1100_thth' in w, True),
    (r'T#bar{T} (1.3 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1300_thth' in w, True),
    (r'T#bar{T} (1.5 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1500_thth' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1700_thth' in w, True),
]

table_block_signal_fs_700 = [
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0700_thth' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtZ', lambda w: 'Integral___TpTp_M-0700_thtz' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHbW', lambda w: 'Integral___TpTp_M-0700_thbw' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tZtZ', lambda w: 'Integral___TpTp_M-0700_noH_tztz' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tZbW', lambda w: 'Integral___TpTp_M-0700_noH_tzbw' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ bWbW', lambda w: 'Integral___TpTp_M-0700_noH_bwbw' in w, True),
]

table_block_signal_fs_1700 = [
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1700_thth' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtZ', lambda w: 'Integral___TpTp_M-1700_thtz' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHbW', lambda w: 'Integral___TpTp_M-1700_thbw' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tZtZ', lambda w: 'Integral___TpTp_M-1700_noH_tztz' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tZbW', lambda w: 'Integral___TpTp_M-1700_noH_tzbw' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ bWbW', lambda w: 'Integral___TpTp_M-1700_noH_bwbw' in w, True),
]

table_block_background = [
    (r'$\mathrm{t\bar{t}}$', lambda w: 'Integral___t#bar{t}' in w),
    ('W + Jets', lambda w: 'Integral___W + jets' in w),
    ('Z + Jets', lambda w: 'Integral___DY + jets' in w),
    ('QCD', lambda w: 'Integral___QCD' in w),
    ('Single t', lambda w: 'Integral___Single t' in w),
]

norm_factors = [
    ('T#bar{T} (0.7 TeV)', (1./normfactors['TpTp_M-0700'])*lumi),
    ('T#bar{T} (0.9 TeV)', (1./normfactors['TpTp_M-0900'])*lumi),
    ('T#bar{T} (1.1 TeV)', (1./normfactors['TpTp_M-1100'])*lumi),
    ('T#bar{T} (1.3 TeV)', (1./normfactors['TpTp_M-1300'])*lumi),
    ('T#bar{T} (1.5 TeV)', (1./normfactors['TpTp_M-1500'])*lumi),
    ('T#bar{T} (1.7 TeV)', (1./normfactors['TpTp_M-1700'])*lumi),
]

def get_table_category_block(hist_path='Histograms'):
    return [
        ('0H category', get_dict('../%s/StackedAll/SidebandRegion' % hist_path, 'ST')),
        ('H1B category', get_dict('../%s/StackedAll/SignalRegion1b' % hist_path, 'ST')),
        ('H2B category', get_dict('../%s/StackedAll/SignalRegion2b' % hist_path, 'ST')),
    ] if varial.settings.style == 'PAS' else [
        ('Preselection', get_dict('../%s/StackedAll/BaseLineSelection' % hist_path, 'ST')),
        ('0H category', get_dict('../%s/StackedAll/SidebandRegion' % hist_path, 'ST')),
        ('H1B category', get_dict('../%s/StackedAll/SignalRegion1b' % hist_path , 'ST')),
        ('H2B category', get_dict('../%s/StackedAll/SignalRegion2b' % hist_path, 'ST')),
    ]

def get_table_category_block_split(chan, hist_path='Histograms'):
    return [
        ('Preselection', get_dict('../%s/StackedAll/BaseLineSelection_%s' % (hist_path, chan), 'ST')),
        ('0H category', get_dict('../%s/StackedAll/SidebandRegion_%s' % (hist_path, chan), 'ST')),
        ('H1B category', get_dict('../%s/StackedAll/SignalRegion1b_%s' % (hist_path, chan) , 'ST')),
        ('H2B category', get_dict('../%s/StackedAll/SignalRegion2b_%s' % (hist_path, chan), 'ST')),
    ]

# table_category_block_comp_fs = [
#     ('0H category', get_dict('../Histograms/StackedAll/SidebandRegion', 'ST')),
#     ('H1B category', get_dict('../Histograms/StackedAll/SignalRegion1b', 'ST')),
#     ('H2B category', get_dict('../Histograms/StackedAll/SignalRegion2b', 'ST')),
# ] if varial.settings.style == 'PAS' else [
#     ('Preselection', get_dict('../Histograms/StackedAll/BaseLineSelection', 'ST')),
#     ('0H category', get_dict('../Histograms/StackedAll/SidebandRegion', 'ST')),
#     ('H1B category', get_dict('../Histograms/StackedAll/SignalRegion1b' , 'ST')),
#     ('H2B category', get_dict('../Histograms/StackedAll/SignalRegion2b', 'ST')),
# ]
