#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools
# import varial.toolinterface

dirname = 'VLQToHiggsPairProd'

varial.settings.rootfile_postfixes += ['.pdf']

current_tag = varial.settings.git_tag

# def new_commit():
#     commit_mess = raw_input('Please enter commit message: ')
#     os.system("git commit -m '%s'", % commit_mess)

# def document_plot(option="none"):
#     if os.system('git diff --quiet') or os.system('git diff --cached --quiet') :
#         commit_opt = raw_input('Changes in git tree detected, want to make a new commit (c), amend (a) or do nothing (N)? ')
#         options = {
#             "c" : new_commit,
#             "C" : new_commit,
#             "a" : amend_commit,
#             "A" : amend_commit,
#             "n" : no_commit,
#             "N" : no_commit,
#             ""  : no_commit
#         }




def make_eff_graphs(wrps):
    token = lambda w: w.legend + ":" + "/".join(w.in_file_path)[:-4]
    subs, tots = {}, {}
    res = []
    for wrp in wrps:
        yield wrp
        if wrp.name.endswith('_sub'):
            t = token(wrp)
            if t in tots:
                res.append(varial.operations.eff((wrp, tots.pop(t))))
            else:
                subs[t] = wrp
        elif wrp.name.endswith('_tot'):
            t = token(wrp)
            if t in subs:
                res.append(varial.operations.eff((subs.pop(t), wrp)))
            else:
                tots[t] = wrp
        if res and not (subs or tots):
            for _ in xrange(len(res)):
                yield res.pop(0)


def norm_histos_to_integral(wrps):
    for wrp in wrps:
        if isinstance(wrp, varial.wrappers.HistoWrapper):
            yield varial.operations.norm_to_integral(wrp)
        else:
            yield wrp


def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def loader_hook(wrps):
    wrps = label_axes(wrps)
    wrps = make_eff_graphs(wrps)
    wrps = norm_histos_to_integral(wrps)
    return wrps


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
    return varial.tools.Plotter(**kws)

<<<<<<< HEAD
tagger = varial.tools.GitTagger()
=======
def create_name(name):
    return name+'v'+varial.settings.git_tag

tagger = varial.tools.GitTagger('/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_2_1_patch4/src/UHH2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')
>>>>>>> 3565e26... Test commit 5

tagger.run()

pl = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    plotter_factory=plotter_factory,
    combine_files=True
)

<<<<<<< HEAD
def create_name(name):
    return name+'v'+varial.settings.git_tag

p = varial.toolinterface.ToolChain(create_name(dirname), [tagger, pl])

pp = varial.toolinterface.ToolChain('SuperChain', [p])


=======
>>>>>>> 3565e26... Test commit 5

time.sleep(1)
<<<<<<< HEAD
pp.run()
=======
pl.run()
>>>>>>> caf8146... Test commit 6
varial.tools.WebCreator().run()
# os.system('rm -r ~/www/%s' % dirname)
# os.system('mv -f %s ~/www' % dirname)
