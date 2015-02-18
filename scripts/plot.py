#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools
import varial.generators as gen
import itertools
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


def loader_hook(wrps):
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

def loader_hook2(wrps):
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
    wrps = norm_histos_to_first_bin(wrps)
    wrps = label_axes(wrps)
    return wrps

def loader_hook3(wrps):
    wrps = itertools.ifilter(lambda w: w.histo.Integral(), wrps)
    wrps = label_axes(wrps)
    return wrps

def loader_hook4(wrps):
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

# use these functions to specifically select histograms for plotting
current_cut = 'AllCuts'

def select_histograms(wrp):
    use_this = True
    if 'NoGenSel-'+current_cut not in wrp.in_file_path:
        use_this = False
    if wrp.name.startswith('cf_') or 'TauHists' in wrp.in_file_path:
        use_this = False
    if 'NoGenSel' not in wrp.in_file_path:
        use_this = False
    if 'GenHists' in wrp.in_file_path and ('NoCuts' not in wrp.in_file_path and 'AllCuts' not in wrp.in_file_path):
        use_this = False
    return use_this

def select_splithistograms(wrp):
    use_this = False
    if 'NoGenSel-'+current_cut not in wrp.in_file_path:
        return False
    if any(n in wrp.in_file_path for n in ['TauHists','TopJetHists']):
        return False
    if 'GenHists' in wrp.in_file_path and (wrp.name.startswith('mu_') or 'parton' in wrp.name):
        use_this = True
    if 'EventHists' in wrp.in_file_path and ('HT' in wrp.name or 'jets' in wrp.name):
        use_this = True
    if 'JetHists' in wrp.in_file_path and any(s in wrp.name for s in ['jet', '1', '2']):
        use_this = True
    if 'MuonHists' in wrp.in_file_path and 'charge' not in wrp.name:
        use_this = True
    return use_this 

def plotter_factory(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook
    kws['plot_setup'] = gen.mc_stack_n_data_sum
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def plotter_factory2(**kws):
    # kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook2
    kws['save_lin_log_scale'] = True
    kws['save_name_func'] = lambda w : w.name + '_norm'
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def plotter_factory3(**kws):
    # kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook3
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def plotter_factory4(**kws):
    kws['filter_keyfunc'] = lambda w: 'TH1' in w.type
    kws['hook_loaded_histos'] = loader_hook4
    kws['save_lin_log_scale'] = True
    # kws['save_log_scale'] = True
    # kws['hook_canvas_pre_build'] = canvas_hook
    # kws['hook_canvas_post_build'] = canvas_hook
    return varial.tools.Plotter(**kws)

def create_name(name):
    return name+'v'+varial.settings.git_tag

    

tagger = varial.tools.GitTagger('/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_2_1_patch4/src/UHH2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

tagger.run()



p1 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    filter_keyfunc=lambda w: not w.name.startswith('cf_'),
    plotter_factory=plotter_factory,
    combine_files=True
)

p2 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=plotter_factory2,
    combine_files=True
)

p3 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname),
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=plotter_factory3,
    combine_files=True
)

p4 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='temp-VLQv15/*.root',
    filter_keyfunc=lambda w: not w.name.startswith('cf_'),
    plotter_factory=plotter_factory4,
    combine_files=False
)

p5 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    filter_keyfunc=lambda w: not w.name.startswith('cf_'),
    plotter_factory=plotter_factory4,
    combine_files=True
)

p6 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='temp-VLQv15/*.root',
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=plotter_factory2,
    combine_files=False
)

p7 = varial.tools.mk_rootfile_plotter(
    name=create_name(dirname)+'split',
    pattern='temp-VLQv15/*.root',
    filter_keyfunc=lambda w: w.name.startswith('cf_') and not w.name.endswith('raw'),
    plotter_factory=plotter_factory3,
    combine_files=False
)

time.sleep(1)
# p1.run()
# p2.run()
# p3.run()
p4.run()
p5.run()
p6.run()
p7.run()
varial.tools.WebCreator().run()
# os.system('rm -r ~/www/TprimeAnalysis/%s' % create_name(dirname))
# os.system('cp -r %s ~/www/TprimeAnalysis/' % create_name(dirname))
