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

cuts = ['NoGenSel-NoCuts', 'NoGenSel-AllCuts'
    ]

varial.settings.defaults_Legend['x_pos'] = 0.80
varial.settings.defaults_Legend['label_width'] = 0.36
varial.settings.defaults_Legend['label_height'] = 0.03
# varial.settings.debug_mode = True
varial.settings.box_text_size = 0.03
varial.settings.colors = {
    'TTJets': 632, 
    'WJets': 878,
    'ZJets': 596, 
    'TpTp_M1000': 870, 
    # 'TpJ_TH_M800_NonTlep': 434,
}


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
    wrps = gen.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path[0],
        legend=lambda w: ('100* ' if 'TpTp_M' in w.sample else '') + w.sample,
        is_signal=lambda w: 'TpTp_M' in w.sample,
        lumi=lambda w: 0.01 if 'TpTp_M' in w.sample else 1.
    )
    # wrps = gen.imap_conditional(wrps, lambda w: 'TpJ_TH_M800' in w.sample, gen.op.norm_to_lumi)
    wrps = label_axes(wrps)
    return wrps

# def loader_hook(wrps):
#     wrps = label_axes(wrps)
#     wrps = gen.gen_make_eff_graphs(wrps)
#     wrps = norm_histos_to_integral(wrps)
#     # wrps = log_scale(wrps)
#     for w in wrps:
#         yield w

def canvas_hook(wrps):
    wrps = log_scale(wrps)
    return wrps


def plotter_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    kws['save_lin_log_scale'] = True
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
    filter_keyfunc=lambda w: w.in_file_path.split('/')[0] in cuts,
    plotter_factory=plotter_factory,
    combine_files=True
)


time.sleep(1)
pl.run()
varial.tools.WebCreator().run()
# os.system('rm -r ~/www/TprimeAnalysis/%s' % create_name(dirname))
# os.system('cp -r %s ~/www/TprimeAnalysis/' % create_name(dirname))
