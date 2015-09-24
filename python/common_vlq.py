import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')


import varial
import varial.history


def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


signal_indicators = ['TpTp']


def add_wrp_info(wrps):
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path.split('/')[0],
        legend=lambda w: w.sample,
        is_signal=lambda w: any(s in w.sample for s in signal_indicators),
        is_data=lambda w: 'Run20' in w.sample,
    )


def merge_decay_channels(wrps, postfixes, suffix=''):
    """histos must be sorted!!"""

    @varial.history.track_history
    def merge_decay_channel(w):
        return w

    def do_merging(buf):
        res = varial.operations.merge(buf)
        res.sample = next(res.sample[:-len(p)]
                          for p in postfixes
                          if res.sample.endswith(p))+suffix
        res.legend = next(res.legend[:-len(p)]
                          for p in postfixes
                          if res.legend.endswith(p))+suffix
        res.file_path = ''
        del buf[:]
        return merge_decay_channel(res)

    buf = []
    for w in wrps:
        if any(w.sample.endswith(p) for p in postfixes):
            buf.append(w)
            if len(buf) == len(postfixes):
                yield do_merging(buf)
        else:
            if buf:
                # print 'WARNING In merge_decay_channels: buffer not empty. ' \
                #       'Flushing remaining items:' + str(buf)
                yield do_merging(buf)
            yield w




def merge_samples_old(wrps):
    wrps = merge_decay_channels(wrps, (
        '_LNu_HT100to200',
        '_LNu_HT200to400',
        '_LNu_HT400to600',
        '_LNu_HT600toInf',
    ))
    wrps = merge_decay_channels(wrps, (
        '_LL_HT100to200',
        '_LL_HT200to400',
        '_LL_HT400to600',
        '_LL_HT600toInf',
    ))
    wrps = merge_decay_channels(wrps, (
        # '_HT250to500',
        '_HT500to1000',
        '_HT1000toInf',
    ))
    return wrps

def merge_samples(wrps):
    wrps = merge_decay_channels(wrps, (
        '_Pt15to30',
        '_Pt30to50',
        '_Pt50to80',
        '_Pt80to120',
        '_Pt120to170',
        '_Pt170to300',
        '_Pt300to470',
        '_Pt470to600',
        '_Pt600to800',
        '_Pt800to1000',
        '_Pt1000to1400',
        '_Pt1400to1800',
        '_Pt1800to2400',
        '_Pt2400to3200',
        '_Pt3200toInf',
    ))
    wrps = merge_decay_channels(wrps, (
        'M10to50',
        'M50toInf',
    ))
    wrps = merge_decay_channels(wrps, (
        '_tChannel',
        '_WAntitop',
        '_WTop',
    ))
    wrps = merge_decay_channels(wrps, (
        '_Mtt0to700',
        '_Mtt700to1000',
        '_Mtt1000toInf',
    ))
    wrps = merge_decay_channels(wrps, (
        '_Ele',
        '_Mu',
        '_Had'
    ))
    return wrps

def norm_to_first_bin(wrp):
    histo = wrp.histo.Clone()
    firstbin = histo.GetBinContent(1)
    histo.Scale(1. / firstbin)
    info = wrp.all_info()
    info["lumi"] /= firstbin
    return varial.wrappers.HistoWrapper(histo, **info)

def norm_histos_to_first_bin(wrps):
    for wrp in wrps:
        if isinstance(wrp, varial.wrappers.HistoWrapper):
            yield norm_to_first_bin(wrp)
        else:
            yield wrp
