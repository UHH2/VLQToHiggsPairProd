import os

import varial.analysis
import varial.generators as gen
import varial.rendering as rnd
import pprint

import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.operations as op
import varial.wrappers
import varial.util as util

from ROOT import THStack, TH2, TLatex

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
    'ST' : {'rebin' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 1000.,
            # 'leg_pos',
            # 'set_leg_2_col' : True
            },
    'ST_rebin_flex' : {
            'y_max_log_fct' : 1000.,
            'set_leg_2_col' : True
            },
    'HT' : {'rebin' : [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.],
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 1000.,
            # 'leg_pos',
            'set_leg_2_col' : True
            },
    'HT_rebin_flex' : {
            'y_max_log_fct' : 1000.,
            # 'leg_pos',
            'set_leg_2_col' : True
            },
    'mass_sj' : {'rebin' : 30,
            'title' : 'groomed Higgs tag mass [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            # 'leg_pos',
            # 'set_leg_2_col' : True
            },
    'nomass_boost_1b_mass' : {'rebin' : 30,
            'title' : 'groomed type-I Higgs tag mass [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            # 'leg_pos',
            # 'set_leg_2_col' : True
            },
    'nomass_boost_2b_mass' : {'rebin' : 15,
            'title' : 'groomed type-II Higgs tag mass [GeV]',
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.2
            },
    'primary_electron_pt' : {
            'title' : 'Primary Electron p_{T} [GeV]',
            },
    'primary_muon_pt' : {
            'title' : 'Primary Muon p_{T} [GeV]',
            },
    'pt' : {
            'rebin' : 30,
            'title' : 'p_{T} leading Higgs tag [GeV]',
            'y_max_log_fct' : 1000.,
            # 'set_leg_2_col' : True,
            'y_max_fct' : 1.5,
            },
    'pt_ld_ak4_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} leading AK4 Jet [GeV]',
            'y_max_log_fct' : 1000.,
            # 'set_leg_2_col' : True,
            'y_max_fct' : 1.5,
            },
    'pt_ld_ak8_jet' : {
            'rebin' : 30,
            'title' : 'p_{T} leading AK8 Jet [GeV]',
            'y_max_log_fct' : 1000.,
            # 'set_leg_2_col' : True,
            'y_max_fct' : 1.5,
            },
    'n_additional_btags_medium' : {
            'title' : 'N(AK4 b tags)',
            'y_max_log_fct' : 1000.,
            'set_leg_2_col' : True
            },
    'n_higgs_tags_1b_med' : {
            'title' : 'N(type-I Higgs tags)',
            'y_max_log_fct' : 1000.,
            'set_leg_2_col' : True
            },
    'n_higgs_tags_2b_med' : {
            'title' : 'N(type-II Higgs tags)',
            # 'y_max_log_fct' : 1000.,
            },
    'n_ak4' : {
            'y_max_log_fct' : 10000.,
            'set_leg_2_col' : True
            # 'y_max_log_fct' : 1000.,
            },
    'nobtag_boost_mass_nsjbtags' : {
            'title' : 'N(subjet b tags)',
            'y_max_log_fct' : 1000.,
            # 'set_leg_2_col' : True
            # 'y_max_log_fct' : 1000.,
            },
    'n_sjbtags_medium' : {
            'title' : 'N(subjet b tags)',
            'y_max_log_fct' : 1000.,
            # 'set_leg_2_col' : True
            # 'y_max_log_fct' : 1000.,
            },

}





signal_indicators = ['TpTp_']

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
            w.legend = 'TT M'+w.legend[7:]
        if w.legend == 'DYJetsToLL' or w.legend == 'DYJets':
            w.legend = 'DY + jets'
        if w.legend == 'WJets':
            w.legend = 'W + jets'
        if w.legend == 'SingleTop':
            w.legend = 'Single t'
        if w.legend == 'TTbar':
            w.legend = 'ttbar '
        yield w

def mod_legend_eff_counts(wrps):
    for w in wrps:
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5] + '#rightarrow tHtH'
        if w.legend.endswith('_thtz'):
            w.legend = w.legend[:-5] + '#rightarrow tHtZ'
        if w.legend.endswith('_thbw'):
            w.legend = w.legend[:-5] + '#rightarrow tHbW'
        if w.legend.endswith('_tztz'):
            w.legend = w.legend[:-9] + '#rightarrow tZtZ'
        if w.legend.endswith('_tzbw'):
            w.legend = w.legend[:-9] + '#rightarrow tZbW'
        if w.legend.endswith('_bwbw'):
            w.legend = w.legend[:-9] + '#rightarrow bWbW'
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

def fix_get_samplename(wrp):
    fname = os.path.basename(wrp.file_path)
    if fname.startswith('uhh2'):
        return fname.split('.')[-2]
    else:
        return os.path.splitext(fname)[0]

def add_wrp_info(wrps, sig_ind=None):
    sig_ind = sig_ind or signal_indicators
    if varial.settings.fix_presel_sample:
        get_samplename = fix_get_samplename
    else:
        get_samplename = vlq_common.get_samplename
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=get_samplename,
        legend=lambda w: w.sample,
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
        bkg_sum = util.integral_and_error(wrp.histo)
        if len(bkg_sum) == 2:
            bkg_sum = (bkg_sum[0]/fct, bkg_sum[1]/fct)
        sys_sum = (util.integral_and_error(wrp.histo_sys_err)
                   if wrp.histo_sys_err
                   else tuple())
        if len(sys_sum) == 2:
            sys_sum = (sys_sum[0]/fct, sys_sum[1]/fct)
        if len(sys_sum) == 2 and len(bkg_sum) >= 1:
            diff = sys_sum[0] - bkg_sum[0]
            sys_up = sys_sum[1] + diff
            sys_down = sys_sum[1] - diff
            sys_sum = (sys_up, -sys_down)
        return [(wrp.sample, bkg_sum + sys_sum)]

    def integral_stack_wrp(wrp):
        for hist in wrp.obj.GetHists():
            fct = 1.
            if hasattr(wrp, 'scl_fct'):
                fct = wrp.scl_fct
            sum_tmp = util.integral_and_error(hist)
            sys_tmp = getattr(wrp, hist.GetTitle()+'__sys', (sum_tmp[0], 0.))
            if len(sum_tmp) == 2:
                diff = sys_tmp[0] - sum_tmp[0]
                sys_up = sys_tmp[1] + diff
                sys_down = sys_tmp[1] - diff
                sys_tmp = (sys_up, -sys_down)
                sum_tmp = (sum_tmp[0]/fct, sum_tmp[1]/fct, sys_tmp[0]/fct, sys_tmp[1]/fct)
            yield hist.GetTitle(), sum_tmp
        bkg_sum = util.integral_and_error(wrp.histo)
        # if len(bkg_sum) == 2:
            # bkg_sum = (bkg_sum[0]*2, bkg_sum[1]*2)
        sys_sum = (util.integral_and_error(wrp.histo_sys_err)
                   if wrp.histo_sys_err
                   else tuple())
        if len(sys_sum) == 2 and len(bkg_sum) >= 1:
            diff = sys_sum[0] - bkg_sum[0]
            sys_up = sys_sum[1] + diff
            sys_down = sys_sum[1] - diff
            sys_sum = (sys_up, -sys_down)
        # if len(sys_sum) == 2:
            # sys_sum = (sys_sum[0]*2, sys_sum[1]*2)
        yield 'bkg_sum', bkg_sum + sys_sum

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
            if not rebin_ind:
                w = op.rebin_nbins_max(w, 60)
        yield w

def leg_2_col(rnd):
    if varial.settings.style != 'AN':
        rnd.legend.SetNColumns(2)
        n_entries = len(rnd.legend.GetListOfPrimitives())
        x_pos   = rnd.dec_par.get('x_pos', varial.settings.defaults_Legend['x_pos'])
        y_pos   = rnd.dec_par.get('y_pos', varial.settings.defaults_Legend['y_pos'])
        width   = rnd.dec_par.get('label_width', varial.settings.defaults_Legend['label_width'])
        height  = rnd.dec_par.get('label_height', varial.settings.defaults_Legend['label_height']) * n_entries / 2.
        rnd.legend.SetX1(x_pos - 3*width/2.)
        rnd.legend.SetY1(y_pos - 0.1*height)
        rnd.legend.SetX2(x_pos + width/2.)
        rnd.legend.SetY2(y_pos + 0.9*height)


def mod_post_canv(grps):
    for g in grps:
        _, y_max = g.y_bounds
        mod_wrp_dict = mod_dict.get(g.name, None)
        if mod_wrp_dict:
            y_min_gr_zero = mod_wrp_dict.get('y_min_gr_zero', None)
            if y_min_gr_zero:
                g.y_min_gr_zero = y_min_gr_zero
            y_max_fct = mod_wrp_dict.get('y_max_fct', None)
            if y_max_fct:
                g.first_drawn.SetMaximum(y_max * y_max_fct)
            y_max_log_fct = mod_wrp_dict.get('y_max_log_fct', None)
            if y_max_log_fct:
                setattr(g.renderers[0], 'y_max_log', y_max * y_max_log_fct)
            set_leg_2_col = mod_wrp_dict.get('set_leg_2_col', None)
            if set_leg_2_col:
                leg_2_col(g)
        if not any(w.is_data for w in g.renderers):
            g.canvas.SetCanvasSize(varial.settings.canvas_size_x, int(16./19.*varial.settings.canvas_size_y))
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


