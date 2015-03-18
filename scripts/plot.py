#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools
import varial.generators as gen
import itertools
from varial.sample import Sample
import varial.analysis as analysis
# import varial.toolinterface

dirname = 'VLQToHiggsPairProd'

varial.settings.rootfile_postfixes += ['.pdf']

varial.settings.git_tag = varial.settings.readgittag('/nfs/dust/cms/user/nowatsd/sFrameNew/SFRAME/new_uhh2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

current_tag = varial.settings.git_tag

cuts = ['NoGenSel-NoCuts', 'NoGenSel-AllCuts'
    ]

# sample definitions
smpls = list()


smpls.append(Sample(
    name='QCD',
    legend='QCD'
))

smpls.append(Sample(
    name='TTJets',
    legend='TTJets'
))

smpls.append(Sample(
    name='WJets',
    legend='WJets'
))

smpls.append(Sample(
    name='ZJets',
    legend='ZJets'
))

analysis.all_samples = dict((s.name, s) for s in smpls)

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

# SELECT HISTOGRAMS TO PLOT HERE!

# use these functions to specifically select histograms for plotting
current_cuts = ['NoCuts'] # 'NoCuts', 'Nminus1-MuonPtCut', 'OneCut-HTCut'
current_hists = ['/ElectronHists']

varial.settings.stacking_order = ['ZJets', 'WJets', 'TTJets', 'QCD']

def select_histograms(wrp):
    use_this = True
    if all('NoGenSel-'+c not in wrp.in_file_path for c in current_cuts):
        use_this = False
    if wrp.name.startswith('cf_'):
        use_this = False
    if all(c not in wrp.in_file_path for c in current_hists):
        use_this = False
    # if ('GenHists' in wrp.in_file_path and not (wrp.name.startswith('mu_') or wrp.name.startswith('genjet_'))):
    #     use_this = False
    # if 'GenHists' in wrp.in_file_path and ('NoCuts' not in wrp.in_file_path and 'Nminus1-BTagCut' not in wrp.in_file_path):
    #     use_this = False
    return use_this

def select_splithistograms(wrp):
    use_this = True
    if all('NoGenSel-'+c not in wrp.in_file_path for c in current_cuts):
        use_this = False
    if wrp.name.startswith('cf_'):
        use_this = False
    if all(c not in wrp.in_file_path for c in current_hists):
        use_this = False
    # if ('GenHists' in wrp.in_file_path and not (wrp.name.startswith('mu_') or wrp.name.startswith('genjet_'))):
    #     use_this = False
    # if 'GenHists' in wrp.in_file_path and ('NoCuts' not in wrp.in_file_path and 'Nminus1-BTagCut' not in wrp.in_file_path):
    #     use_this = False
    return use_this 



# SOME FUNCTIONS TO MANIPULATE HISTOGRAMS

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

def norm_cf_plots(wrps):
    for w in wrps:
        if w.name.startswith('cf_') and isinstance(w, varial.wrappers.HistoWrapper):
            yield varial.operations.norm_to_integral(w)
        else:
            yield w


# HOOK FUNCTIONS FOR PLOTTER_FACTORIES; manipulate histograms here

def for_stacked_hook(wrps):
    # wrps = norm_cf_plots(wrps)
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
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

def norm_cf_hook(wrps):
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
    wrps = norm_histos_to_first_bin(wrps)
    wrps = label_axes(wrps)
    return wrps

def do_nothing_hook(wrps):
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
    wrps = label_axes(wrps)
    return wrps

def for_eff_plots_hook(wrps):
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
    wrps = gen.gen_add_wrp_info(
        wrps,
        sample=lambda w: w.file_path.split('.')[-2],
        analyzer=lambda w: w.in_file_path[0],
        legend=lambda w: ('100* ' if 'TpTp_M' in w.sample else '') + w.sample,
        is_signal=lambda w: 'TpTp_M' in w.sample,
        lumi=lambda w: 0.01 if 'TpTp_M' in w.sample else 1.
    )
    wrps = gen.gen_make_eff_graphs(wrps)
    wrps = label_axes(wrps)
    return wrps


# def calc_stack_order(wrps):
#     for w in wrps:


# def stack_by_max(wrps):
#     wrps = calc_stack_order(wrps)
#     wrps = gen.mc_stack_n_data_sum(wrps)
#     return wrps


# PLOTTER FACTORIES; select here in general which histograms to plot, how to manipulate them a.s.o.

def stack_histos_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = for_stacked_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def norm_cf_factory(**kws):
    # kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = norm_cf_hook
    kws['save_lin_log_scale'] = True
    kws['save_name_func'] = lambda w : w.name + '_norm'
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def do_nothing_factory(**kws):
    # kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = do_nothing_hook
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def for_eff_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = for_eff_plots_hook
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def create_name(name):
    return name+'v'+varial.settings.git_tag

    

tagger = varial.tools.GitTagger('/nfs/dust/cms/user/nowatsd/sFrameNew/SFRAME/new_uhh2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

tagger.run()



p1 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    # filter_keyfunc=lambda w: not w.name.startswith('cf_'),
    filter_keyfunc=select_histograms,
    plotter_factory=stack_histos_factory,
    combine_files=True
)

p2 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=norm_cf_factory,
    combine_files=True
)

p3 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=do_nothing_factory,
    combine_files=True
)

p4 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='v1.19_unmerged_files/*.root',
    filter_keyfunc=select_splithistograms,
    plotter_factory=for_eff_factory,
    combine_files=False
)

p5 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    # filter_keyfunc=lambda w: not w.name.startswith('cf_'),
    filter_keyfunc=select_splithistograms,
    plotter_factory=for_eff_factory,
    combine_files=True
)

p6 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='v1.19_unmerged_files/*.root',
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=norm_cf_factory,
    combine_files=False
)

p7 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='v1.19_unmerged_files/*.root',
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=do_nothing_factory,
    combine_files=False
)

time.sleep(1)
p1.run()
# p2.run()
# p3.run()
# p4.run()
p5.run()
# p6.run()
# p7.run()
varial.tools.WebCreator().run()
# os.system('rm -r ~/www/TprimeAnalysis/%s' % create_name(dirname))
# os.system('cp -r %s ~/www/TprimeAnalysis/' % create_name(dirname))
