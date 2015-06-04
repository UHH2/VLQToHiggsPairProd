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


signal_indicators = ['_M1000']


def add_wrp_info(wrps):
    return varial.generators.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path.split('/')[0],
        legend=lambda w: w.sample,
        is_signal=lambda w: any(s in w.sample for s in signal_indicators),
    )


@varial.history.track_history
def merge_decay_channel(w):
    return w

def merge_decay_channels(wrps, postfixes):
    """histos must be sorted!!"""
    buf = []
    for w in wrps:
        if any(w.sample.endswith(p) for p in postfixes):
            # print 'Append '+w.sample
            buf.append(w)
            if len(buf) == len(postfixes):
                res = varial.operations.sum(buf)
                res.sample = next(res.sample[:-len(p)]
                                  for p in postfixes
                                  if res.sample.endswith(p))
                res.legend = next(res.legend[:-len(p)]
                                  for p in postfixes
                                  if res.legend.endswith(p))
                res.file_path = ''
                buf = []
                yield merge_decay_channel(res)
        else:
            if buf: print "WARNING: buffer not empty!"
            yield w




def merge_samples(wrps):
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
        '_HT250to500',
        '_HT500to1000',
        '_HT1000toInf',
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
