#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy
import ctypes
import pprint

import varial.settings
import varial.tools
import varial.generators as gen
import varial.rendering as rnd
# import varial.analysis as analysis
# from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
from varial.extensions.sframe import SFrame
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.settings
# import common_vlq
import tptp_settings
import tptpsframe_runner
# import final_plotting
import plot_new as plot
import common_plot_new as common_plot
# import tptp_sframe 
# import compare_crs
import analysis
import tex_content_new as tex_content

from ROOT import TLatex, TH2


sframe_cfg = '/afs/desy.de/user/n/nowatsd/xxl-af-cms/SFrameUHH2/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpHiggsTagEfficiency.xml'

basenames = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'MC.TpTp_M-0700',
    'MC.TpTp_M-0800',
    'MC.TpTp_M-0900',
    'MC.TpTp_M-1000',
    'MC.TpTp_M-1100',
    'MC.TpTp_M-1200',
    'MC.TpTp_M-1300',
    'MC.TpTp_M-1400',
    'MC.TpTp_M-1500',
    'MC.TpTp_M-1600',
    'MC.TpTp_M-1700',
    'MC.TpTp_M-1800',
    'MC.TTbar',
    'MC.WJets',
    'MC.QCD'
    ])

varial.settings.colors.update({
    'TTbar': 632,
    'WJets': 860,
})


def apply_split_pad_styles(cnv_wrp):
    main, scnd = cnv_wrp.main_pad, cnv_wrp.second_pad

    main.SetTopMargin(0.125)
    main.SetBottomMargin(bottom_pad_height)
    #main.SetRightMargin(0.04)
    #main.SetLeftMargin(0.16)

    scnd.SetTopMargin(0.)
    scnd.SetBottomMargin(0.375)
    #scnd.SetRightMargin(0.04)
    #scnd.SetLeftMargin(0.16)
    scnd.SetRightMargin(main.GetRightMargin())
    scnd.SetLeftMargin(main.GetLeftMargin())
    scnd.SetGridy()

    first_obj = cnv_wrp.first_obj
    first_obj.GetYaxis().CenterTitle(1)
    first_obj.GetYaxis().SetTitleSize(0.05)
    first_obj.GetYaxis().SetTitleOffset(1.)
    first_obj.GetYaxis().SetLabelSize(0.055)
    first_obj.GetXaxis().SetNdivisions(505)

varial.settings.apply_split_pad_styles = apply_split_pad_styles



def sort_legend_signal(w):
    if 'TeV' in w:
        mass = w[-8:-5]
        return -float(mass)
    else:
        return -100

varial.settings.defaults_Legend.update({
    'y_pos': 0.75,
    'x_pos': 0.33,
    'label_width': 0.25,
    'label_height': 0.05,
    'box_text_size' : 0.036,
    'sort_legend' : sort_legend_signal,
    })
# colors_mu = [797, 434, 409]
# colors_el = [625, 596, 617]
all_colors = [797, 434, 409, 625, 596, 617]
markers = [(21, 0.8), (22, 1.), (23, 1.), (20, 0.8), (24, 0.8), (25, 0.8), (26, 0.8)]

def add_eff_to_wrp(wrps):
    for w in wrps:
        if w.name.endswith('_incl_eff'):
            eff_x, eff_y = ctypes.c_double(), ctypes.c_double()
            w.graph.GetPoint(0, eff_x, eff_y)
            y_plus = w.graph.GetErrorYhigh(0)
            y_minus = w.graph.GetErrorYlow(0)
            setattr(w, w.sample+'_efficiency', (eff_y.value, y_plus, -y_minus))
        yield w

def mod_title(wrps):
    for w in wrps:
        if 'GenPart' in w.in_file_path:
            x_ax_pre = 'Gen Higgs'
        else:
            x_ax_pre = 'AK8 Jet'
        if 'pt' in w.name:
            x_ax_post = ' p_{T} [GeV]'
        elif 'eta' in w.name:
            x_ax_post = ' #eta'
        elif 'mass' in w.name:
            x_ax_post = ' Mass [GeV]'
        elif 'nsjbtags' in w.name:
            x_ax_post = ' N(b-tagged subjets)'
        else:
            x_ax_post = ''
        if isinstance(w, varial.wrappers.HistoWrapper):
            w.histo.GetXaxis().SetTitle(x_ax_pre+x_ax_post)
        elif isinstance(w, varial.wrappers.GraphWrapper):
            w.graph.GetXaxis().SetTitle(x_ax_pre+x_ax_post)

        if '1b' in w.name:
            y_ax_post = '(H-tag, #geq 1 b-tagged subjets)'
        elif '2b' in w.name:
            y_ax_post = '(H-tag, 2 b-tagged subjets)'
        if 'eff' in w.name:
            if isinstance(w, varial.wrappers.HistoWrapper):
                w.histo.GetYaxis().SetTitle('Efficiency '+y_ax_post)
            elif isinstance(w, varial.wrappers.GraphWrapper):
                w.graph.GetYaxis().SetTitle('Efficiency '+y_ax_post)

        yield w


rebin_list_pt = list(i for i in xrange(0, 1000, 40))
rebin_list_pt += list(i for i in xrange(1000, 1600, 120))
rebin_list_pt += list(i for i in xrange(1600, 2400, 240))


def rebin(wrps):
    for w in wrps:
        if '_pt_' in w.name and not 'TH2' in w.type:
            new_w_flex = op.rebin(w, rebin_list_pt, True)
            suffix = w.name[-4:]
            new_w_flex.name = w.name[:-4]+'_rebin_flex'+suffix
            new_w_flex.in_file_path = w.in_file_path[:-4]+'_rebin_flex'+suffix
            yield new_w_flex
        yield w

def rebin_fix(wrps):
    for w in wrps:
        if '_pt_' in w.name:
            new_w_flex = op.rebin_nbins_max(w, 30)
            yield new_w_flex
        yield w

def mk_marker(wrps):
    for w in wrps:
        if isinstance(w, wrappers.GraphWrapper):
            w.graph.SetMarkerStyle(1)
        yield w

def add_eff_to_info(canvas_builders):

    for cnv in canvas_builders:
        # TODO when rendering goes generator
        # for r in cnv._renderers:
        #     for sample, eff in r.__dict__.iteritems():
        #         if sample.endswith('_efficiency'):
        #             print sample, eff
        cnv.__dict__.update(dict(
            (sample, eff)
            for r in cnv._renderers
            if isinstance(r, rnd.GraphRenderer)  # applies also to StackRnd.
            for sample, eff in r.__dict__.iteritems()
            if sample.endswith('_efficiency')
        ))
        # pprint.pprint(cnv.__dict__.keys(
        # for r in cnv._renderers:
        #     for sample, eff in r.__dict__.iteritems():
        #         if sample.endswith('_efficiency'):
        #             print sample, eff))
        yield cnv


def mk_name(wrp):
    if wrp.is_signal:
        return 'sig_'
    else:
        return 'bkg_'

def marker_style(wrps, markers=markers):
    n = 0
    for wrp in wrps:
        mrk = markers[n % len(markers)]
        n += 1
        if isinstance(wrp, wrappers.GraphWrapper):
            wrp.graph.SetMarkerStyle(mrk[0])
            wrp.graph.SetMarkerSize(mrk[1])
            wrp.draw_option_legend = 'ple'
        yield wrp

def marker_col(wrps):
    n = 0
    for wrp in wrps:
        # if 'electron' in wrp.name:
        #     col = colors_el[n % len(colors_el)]
        # elif 'muon' in wrp.name:
        #     col = colors_mu[n % len(colors_mu)]
        # else:
        col = all_colors[n % len(all_colors)]
        n += 1
        wrp.obj.SetLineColor(col)
        wrp.obj.SetMarkerColor(col)
        yield wrp

def plot_grouper_sep_sig_bkg(wrps):
    # if separate_th2:
    #     wrps = rename_th2(wrps)
    return gen.group(wrps, key_func=lambda w: mk_name(w)+'___'+w.in_file_path)

def mod_cnv_postbuild(cnvs):
    cnvs = common_plot.add_sample_integrals(cnvs)
    cnvs = add_eff_to_info(cnvs)
    return cnvs


def plot_setup(grps):
    grps = (marker_col(ws) for ws in grps)
    grps = (marker_col(ws) for ws in grps)
    grps = (marker_style(ws, markers) for ws in grps)
    grps = list(grps)
    return grps

def loader_hook_eff(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)
    # wrps = common_plot.mod_title(wrps)
    # wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    # wrps = gen.gen_make_th2_projections(wrps)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mod_title(wrps)
    # wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    # wrps = mk_marker(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # # if varial.settings.merge_decay_channels:
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False)
        # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    # wrps = itertools.ifilter(lambda w: not any(w.sample.endswith(g) for g in ['_other']), wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: mk_name(w)+'___'+w.in_file_path)
    return wrps

def plotter_factory_eff():

	def tmp(**kws):
	    # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
	    kws['filter_keyfunc'] = lambda w: 'HiggsTagEfficiencyPreGenPartHiggsBsInJet' in w.in_file_path
	    kws['hook_loaded_histos'] = loader_hook_eff
	    kws['plot_grouper'] = plot_grouper_sep_sig_bkg
	    kws['plot_setup'] = plot_setup
	    # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
	    # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
	    # kws['y_axis_scale'] = 'lin'
	    kws['hook_canvas_post_build'] = mod_cnv_postbuild
	    # kws['hook_canvas_post_build'] = canvas_setup_post
	    # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
	    kws['save_name_func'] = lambda w: mk_name(w._renderers[0])+w.name
	    kws['canvas_post_build_funcs'] = [
                    rnd.mk_legend_func(),
                    # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.79, 0.89, "#scale[0.45]{(13 TeV)}")),
                    ]
	    kws['mod_log'] = common_plot.mod_log_usr()
	    return varial.tools.Plotter(stack=False, **kws)
	return tmp

def sframe_setup(outputdir = '', allowed_datasets=None, count = '10000', categories=None, cacheable='False'):
    def tmp_func(element_tree):
        # set_analysis_module(element_tree, analysis_module)
        tptpsframe_runner.set_cacheable_false(element_tree, cacheable)
        tptpsframe_runner.set_output_dir(element_tree, outputdir)
        tptpsframe_runner.clean_input_data(element_tree, allowed_datasets)
        # make_higgs_split_item(element_tree, 'TpTp', final_states_to_split_into_tp)
        # make_higgs_split_item(element_tree, 'BpBp', final_states_to_split_into_bp)
        tptpsframe_runner.do_set_eventnumber(element_tree, count)
        # set_uncert(element_tree, uncert_name)
        if categories:
            tptpsframe_runner.do_set_cat(element_tree, " ".join(categories))
    return tmp_func

class MySFrameBatch(SFrame):

    def __init__(self, sel_type='', **kws):
        super(MySFrameBatch, self).__init__(**kws)
        self.sel_type = sel_type

    def configure(self):
        self.xml_doctype = self.xml_doctype +"""
<!--
   <ConfigParse NEventsBreak="50000" FileSplit="0" AutoResubmit="0" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="dominik.nowatschin@cern.de" Notification="as" Workdir="workdir"/>
-->
"""

        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt

def run_sframe(name='Test'):
    samples = [
        # 'TpTp_M-0700',
        'TpTp_M-0800',
        # 'TpTp_M-0900',
        # 'TpTp_M-1000',
        # 'TpTp_M-1100',
        'TpTp_M-1200',
        # 'TpTp_M-1300',
        # 'TpTp_M-1400',
        # 'TpTp_M-1500',
        'TpTp_M-1600',
        # 'TpTp_M-1700',
        # 'TpTp_M-1800',
        'TTbar',
        # 'WJets_LNu_HT2500ToInf'
        'WJets',
        'QCD'
    ]

    sframe = MySFrameBatch(
        cfg_filename=sframe_cfg,
        # xml_tree_callback=set_uncert_func(uncert),
        xml_tree_callback=sframe_setup(outputdir='./', allowed_datasets=samples, count='-1', cacheable='False'),
        name='SFrame',
        add_aliases_to_analysis= False,
        # name='SFrame_' + uncert,
        halt_on_exception=False,
        )
    # sframe = varial.tools.ToolChainParallel('SFrame', 
    #     list(SFrame(
    #             cfg_filename=sframe_cfg,
    #             # xml_tree_callback=set_uncert_func(uncert),
    #             xml_tree_callback=sframe_setup(outputdir='./', count='10000', allowed_datasets=[a], cacheable='True'),
    #             name='workdir_'+a,
    #             add_aliases_to_analysis=False,
    #             # name='SFrame_' + uncert,
    #             halt_on_exception=False)
    #         for a in samples)
    #     )

    
    def mk_tc_tex(source_dir):
        tc_tex = [
            tex_content.mk_plot_ind(
                (
                    ('htag_eff_1b_mu', os.path.join(source_dir, 'Plots/StackedAll/Mu45_Baseline/HiggsTagEfficiencyPreGenPartHiggsBsInJet/sig_ak8_1b_pt_rebin_flex_eff_lin.pdf')),
                    ('htag_eff_1b_el', os.path.join(source_dir, 'Plots/StackedAll/El45_Baseline/HiggsTagEfficiencyPreGenPartHiggsBsInJet/sig_ak8_1b_pt_rebin_flex_eff_lin.pdf')),
                    ('htag_eff_2b_mu', os.path.join(source_dir, 'Plots/StackedAll/Mu45_Baseline/HiggsTagEfficiencyPreGenPartHiggsBsInJet/sig_ak8_2b_pt_rebin_flex_eff_lin.pdf')),
                    ('htag_eff_2b_el', os.path.join(source_dir, 'Plots/StackedAll/El45_Baseline/HiggsTagEfficiencyPreGenPartHiggsBsInJet/sig_ak8_2b_pt_rebin_flex_eff_lin.pdf')),
                ),
                name='HiggsTagEffPlots'),
            
        ]
        tc_tex = varial.tools.ToolChain('CopyPlots', [
            varial.tools.ToolChain('TexThesis', tc_tex),
            varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/xxl-af-cms/PlotsToInspect', src='../../Plots/StackedAll/Mu45_Baseline/*', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa --delete', name='CopyToolInspect'),
            varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
            ])
        return tc_tex 

    return varial.tools.ToolChain(name, [
        sframe,
        Hadd(
                src_glob_path='../SFrame/workdir*/uhh2.AnalysisModuleRunner.*.root',
                basenames=basenames,
                add_aliases_to_analysis=False,
                samplename_func=plot.get_samplename,
                # filter_keyfunc=lambda w: any(f in w for f in samples_to_plot)
                # overwrite=False
            ),
        varial.tools.ToolChain(
            'Plots',
            lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_eff())
        ),
        mk_tc_tex(name)
    ])




def plot_only(version='Test', pattern=''):
    plots = varial.tools.ToolChain(
        'Plots',
        lazy_eval_tools_func=plot.mk_plots(pattern=pattern, web_create=True, plotter_factory=plotter_factory_eff())
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots
        ]
    )
    return tc

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    src_dir = sys.argv[1]
    if len(sys.argv) > 2:
        final_dir = sys.argv[2]
    # all_tools = plot_only(version=final_dir, pattern=src_dir)
    all_tools = run_sframe(src_dir)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()