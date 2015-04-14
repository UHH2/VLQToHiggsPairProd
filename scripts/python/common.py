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
    )


@varial.history.track_history
def merge_decay_channel(w):
    return w

def merge_decay_channels(wrps, postfixes=('_Tlep', '_NonTlep')):
    """histos must be sorted!!"""
    buf = []
    for w in wrps:
        if any(w.sample.endswith(p) for p in postfixes):
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
            yield w
