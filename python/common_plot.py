import os

import varial.analysis
import varial.generators as gen
import varial.rendering as rnd

import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.operations as op
import varial.wrappers

from ROOT import THStack

# common_datasets_to_plot = [
#     'Run2015D',
#     'TpTp_M-0700',
#     # 'TpTp_M-0800',
#     # 'TpTp_M-0900',
#     # 'TpTp_M-1000',
#     # 'TpTp_M-1100',
#     'TpTp_M-1200',
#     # 'TpTp_M-1300',
#     # 'TpTp_M-1400',
#     # 'TpTp_M-1500',
#     # 'TpTp_M-1600',
#     'TpTp_M-1700',
#     # 'TpTp_M-1800',
#     # 'QCD_Pt15to30',
#     # 'QCD_Pt30to50',
#     # 'QCD_Pt50to80',
#     'QCD',
#     # 'TTbar',
#     'TTbar',
#     'WJets',
#     'ZJets',
#     'SingleTop',
# ]

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


def norm_smpl(wrps, smpl_fct=None, norm_all=1.):
    for w in wrps:
        if smpl_fct:
            for fct_key, fct_val in smpl_fct.iteritems():
                if fct_key in w.sample:
                    # if w.analyzer = 'NoSelection' or
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
        if w.legend.endswith('_thth'):
            w.legend = w.legend[:-5]
        if w.legend.endswith('_thX'):
            w.legend = w.legend[:-4]
        if w.legend == 'DYJetsToLL' or w.legend == 'DYJets':
            w.legend = 'DY + Jets'
        if w.legend == 'WJets':
            w.legend = 'W + Jets'
        if w.legend == 'SingleTop':
            w.legend = 'Single T'
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
        if w.histo.GetXaxis().GetTitle() == 'N(non-overlapping medium b-tags)':
            w.histo.GetXaxis().SetTitle('N(AK4 b-tags)')
        yield w

def mod_bin(wrps):
    for w in wrps:
        # print w.histo.GetXaxis.GetTitle()
        if w.in_file_path == 'SignalRegion2b_Mu45/ST':
            w = op.rebin_nbins_max(w, 20)
        if w.in_file_path.endswith('mass_sj'):
            w = op.rebin_nbins_max(w, 30)
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
        return [(wrp.legend, wrp.obj.Integral()/fct)]

    def integral_stack_wrp(wrp):
        for hist in wrp.obj.GetHists():
            fct = 1.
            if hasattr(wrp, 'scl_fct'):
                fct = wrp.scl_fct
            yield hist.GetTitle(), hist.Integral()/fct

    def integral(wrp):
        if isinstance(wrp, rnd.StackRenderer):
            return integral_stack_wrp(wrp)
        else:
            return integral_histo_wrp(wrp)

    for cnv in canvas_builders:
        # TODO when rendering goes generator
        cnv.renderers[0].__dict__.update(dict(
            ('Integral__' + legend, integ)
            for r in cnv.renderers
            if isinstance(r, rnd.HistoRenderer)  # applies also to StackRnd.
            for legend, integ in integral(r)
        ))
        yield cnv




