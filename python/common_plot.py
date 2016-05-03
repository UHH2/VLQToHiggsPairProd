import os

import varial.analysis
import varial.generators as gen
import varial.rendering as rnd

import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.operations as op
import varial.wrappers
import varial.util as util

from ROOT import THStack, TH2

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
            w.legend = "Background"
        yield w

# @history.track_history
def scale_signal(wrp, fct=1.):
    if fct >= 5:
        fct = int(fct)
        if fct % 5 > 2:
            fct += fct % 5
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
    if fct > 1:
        wrp.legend +=' (%.2g pb)' % fct
    elif fct < 1:
        wrp.legend +=' (%.1g pb)' % fct

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
        if w.is_signal and 'SignalRegion2b' in w.in_file_path and w.in_file_path.endswith('ST'):
            scale_signal(w, 2.)            
        elif w.is_signal:
            scale_signal(w, 20.) 
        yield w


def mod_legend(wrps):
    for w in wrps:
        if w.legend.startswith('MC_'):
            w.legend = w.legend[3:]
        if w.is_data:
            w.legend = 'data'
        if w.legend.startswith('TpTp'):
            w.legend = 'TT M'+w.legend[7:]
        # if w.legend.endswith('_thth'):
            # w.legend = w.legend[:-5] + ' tH only'
            # w.legend = w.legend[:-5]
        # if w.legend.endswith('_thX'):
        #     w.legend = w.legend[:-4] + ' tH+X'
        # if w.legend.endswith('_other'):
        #     w.legend = w.legend[:-6] + ' other'
        # if w.legend.endswith('_incl'):
        #     w.legend = w.legend[:-5] + ' incl.'
        if w.legend == 'DYJetsToLL' or w.legend == 'DYJets':
            w.legend = 'DY + jets'
        if w.legend == 'WJets':
            w.legend = 'W + jets'
        if w.legend == 'SingleTop':
            w.legend = 'Single T'
        yield w

def mod_legend_eff_counts(wrps):
    for w in wrps:
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5] + ' tHtH'
        if w.legend.endswith('_thtz'):
            w.legend = w.legend[:-5] + ' tHtZ'
        if w.legend.endswith('_thbw'):
            w.legend = w.legend[:-5] + ' tHbW'
        if w.legend.endswith('_tztz'):
            w.legend = w.legend[:-9] + ' tZtZ'
        if w.legend.endswith('_tzbw'):
            w.legend = w.legend[:-9] + ' tZbW'
        if w.legend.endswith('_bwbw'):
            w.legend = w.legend[:-9] + ' bWbW'
        if w.legend.endswith('_thX'):
            w.legend = w.legend[:-4] + ' tH+X'
        if w.legend.endswith('_other'):
            w.legend = w.legend[:-6] + ' other'
        if w.legend.endswith('_incl'):
            w.legend = w.legend[:-5] + ' incl.'
        yield w

def mod_legend_no_thth(wrps):
    for w in wrps:
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5]
        yield w

def mod_title(wrps):
    for w in wrps:
        # print w.histo.GetXaxis.GetTitle()
        if w.histo.GetXaxis().GetTitle() == 'N sjbtags medium':
            w.histo.GetXaxis().SetTitle('N(subjet b-tags)')
        if w.histo.GetXaxis().GetTitle() == 'mass sj':
            w.histo.GetXaxis().SetTitle('groomed AK8 jet mass [GeV]')
        if w.histo.GetXaxis().GetTitle() == 'ST':
            w.histo.GetXaxis().SetTitle('ST [GeV]')
        if w.histo.GetXaxis().GetTitle() == 'HT':
            w.histo.GetXaxis().SetTitle('HT [GeV]')
        if w.histo.GetXaxis().GetTitle() == 'N(non-overlapping medium b-tags)':
            w.histo.GetXaxis().SetTitle('N(AK4 b-tags)')
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
        return [(wrp.legend, bkg_sum + sys_sum)]

    def integral_stack_wrp(wrp):
        for hist in wrp.obj.GetHists():
            fct = 1.
            if hasattr(wrp, 'scl_fct'):
                fct = wrp.scl_fct
            tmp = util.integral_and_error(hist)
            if len(tmp) == 2:
                tmp = (tmp[0]/fct, tmp[1]/fct)
            yield hist.GetTitle(), tmp
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
            ('Integral___' + legend, integ)
            for r in cnv.renderers
            if isinstance(r, rnd.HistoRenderer)  # applies also to StackRnd.
            for legend, integ in integral(r)
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
    st_bounds = [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.]
    ht_bounds = [0., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500.]
    nak4_bounds = list(x - 0.5 for x in xrange(0, 7))+[13.5]
    for w in wrps:
        if w.in_file_path.endswith('ST'):
            new_w = op.rebin_nbins_max(w, 20)
            # new_w = op.rebin(w, st_bounds, True)
            new_w.name = 'ST_rebin'
            new_w.in_file_path = w.in_file_path.replace('ST', 'ST_rebin')
            yield new_w
            # new_w = op.rebin_nbins_max(w, 20)
            new_w_flex = op.rebin(w, st_bounds, True)
            new_w_flex.name = 'ST_rebin_flex'
            new_w_flex.in_file_path = w.in_file_path.replace('ST', 'ST_rebin_flex')
            yield new_w_flex
        if w.in_file_path.endswith('/HT') and not isinstance(w.histo, TH2):
            new_w = op.rebin_nbins_max(w, 20)
            # new_w = op.rebin(w, st_bounds, True)
            new_w.name = 'HT_rebin'
            new_w.in_file_path = w.in_file_path.replace('HT', 'HT_rebin')
            yield new_w
            # new_w = op.rebin_nbins_max(w, 20)
            new_w_flex = op.rebin(w, ht_bounds, True)
            new_w_flex.name = 'HT_rebin_flex'
            new_w_flex.in_file_path = w.in_file_path.replace('HT', 'HT_rebin_flex')
            yield new_w_flex
        if w.in_file_path.endswith('/ht_gen_reco') and not isinstance(w.histo, TH2):
            new_w = op.rebin_nbins_max(w, 20)
            # new_w = op.rebin(w, st_bounds, True)
            new_w.name = 'ht_gen_reco_rebin'
            new_w.in_file_path = w.in_file_path.replace('ht_gen_reco', 'ht_gen_reco_rebin')
            yield new_w
            # new_w = op.rebin_nbins_max(w, 20)
            new_w_flex = op.rebin(w, st_bounds, True)
            new_w_flex.name = 'ht_gen_reco_rebin_flex'
            new_w_flex.in_file_path = w.in_file_path.replace('ht_gen_reco', 'ht_gen_reco_rebin_flex')
            yield new_w_flex
        if w.in_file_path.endswith('n_ak4'):
            new_w = op.rebin(w, nak4_bounds, True)
            new_w.name = 'n_ak4_rebin'
            new_w.in_file_path = w.in_file_path.replace('n_ak4', 'n_ak4_rebin')
            yield new_w 
        if w.in_file_path.endswith('primary_lepton_pt'):
            w = op.rebin(w, list(x * 30 for x in xrange(0, 31)), True)
        if (w.in_file_path.endswith('_jet') or w.in_file_path.endswith('mass_sj')) and not isinstance(w.histo, TH2):
            w = op.rebin_nbins_max(w, 30)
        elif not isinstance(w.histo, TH2):
            w = op.rebin_nbins_max(w, 60)
        yield w




