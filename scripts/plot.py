#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools
import varial.generators as gen
# import varial.toolinterface

dirname = 'VLQToHiggsPairProd'

varial.settings.rootfile_postfixes += ['.pdf']

varial.settings.git_tag = varial.settings.readgittag('/nfs/dust/cms/user/nowatsd/sFrameNew/SFRAME/uhh2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

current_tag = varial.settings.git_tag

cuts = ['NoCuts', 'FinalGenSelNoCuts',
    'GenNoCuts', 'GenFinalGenSelection',
    'OneElectronCut', 'FinalGenSelOneElectronCut',
    'OneElNminusBTagCut', 'FinalGenSelOneElNminusBTagCut',
    'OneElectronFinalSelection', 'FinalGenSelOneElectronFinalSelection'
    ]

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


def log_scale(wrps):
    for wrp in wrps:
        print type(wrp)
        yield wrp

# def make_eff_graphs(wrps):
#     def token(w):
#         token_str = "/".join(w.in_file_path)
#         token_str = token_str.replace('_sub_', '_')
#         token_str = token_str.replace('_tot_', '_')
#         return w.legend + ":" + token_str
#     subs, tots = {}, {}
#     res = []
#     for wrp in wrps:
#         yield wrp
#         if wrp.name.endswith('_sub'):
#             t = token(wrp)
#             if t in tots:
#                 res.append(varial.operations.eff((wrp, tots.pop(t))))
#             else:
#                 subs[t] = wrp
#         elif wrp.name.endswith('_tot'):
#             t = token(wrp)
#             if t in subs:
#                 res.append(varial.operations.eff((subs.pop(t), wrp)))
#             else:
#                 tots[t] = wrp

#         # if subs:
#         #     print 'subs: ', list(subs.keys())
#         # if tots:
#         #     print 'tots: ', list(tots.keys())
#         # if res:
#         #     print 'res: ', res
#         if res and not (subs or tots):
#             for _ in xrange(len(res)):
#                 yield res.pop(0)


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
    wrps = gen.gen_make_eff_graphs(wrps)
    wrps = norm_histos_to_integral(wrps)
    # wrps = log_scale(wrps)
    for w in wrps:
        yield w

def canvas_hook(wrps):
    wrps = log_scale(wrps)
    return wrps


def plotter_factory(**kws):
    kws['hook_loaded_histos'] = loader_hook
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def create_name(name):
    return name+'v'+varial.settings.git_tag

    

tagger = varial.tools.GitTagger('/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_2_1_patch4/src/UHH2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

tagger.run()

pl = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    # filter_keyfunc=lambda w: w.in_file_path.split('/')[0] in cuts,
    plotter_factory=plotter_factory,
    combine_files=True
)


time.sleep(1)
pl.run()
varial.tools.WebCreator().run()
os.system('rm -r ~/www/TprimeAnalysis/%s' % create_name(dirname))
os.system('cp -r %s ~/www/TprimeAnalysis/' % create_name(dirname))
