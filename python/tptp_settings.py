from varial import settings
# from varial.sample import Sample
import varial.analysis as analysis
import UHH2.VLQSemiLepPreSel.vlq_settings
import ROOT
import ctypes

settings.rootfile_postfixes = ['.root', '.png', '.pdf']

settings.__setattr__('asymptotic', True)
settings.__setattr__('merge_decay_channels', True)
settings.__setattr__('plot_obs', True)
settings.__setattr__('fix_presel_sample', False)
settings.__setattr__('do_norm_plot', False)
settings.__setattr__('flex_sig_norm', False)
settings.__setattr__('cutflow_precision', {})
settings.__setattr__('eff_precision', {})
settings.__setattr__('lookup_aliases', 'aliases.in.*')
settings.__setattr__('style', 'AN')

settings.cutflow_precision.update({
    'TpTp_M-0700' : "%17.1f",
    'TpTp_M-1000' : "%17.1f",
    'TpTp_M-1300' : "%17.2f",
    'TpTp_M-1700' : "%17.3f",
    })

settings.pretty_names.update({
    'no sel._tex' : 'no sel.',
    'trigger_accept_el45_tex' : 'Trigger',
    'trigger_accept_mu45_tex' : 'Trigger',
    'primary_lepton_pt_tex' : r'$p_{\mathrm{T}}$(Lepton)',
    'primary_electron_pt_tex' : r'$p_{\mathrm{T}}$(Electron)',
    'primary_muon_pt_tex' : r'$p_{\mathrm{T}}$(Muon)',
    'pt_ld_ak4_jet_tex' : r'$p_{\mathrm{T}}$(1st AK4 jet)',
    'pt_subld_ak4_jet_tex' : r'$p_{\mathrm{T}}$(2nd AK4 jet)',
    '2D cut_tex' : '2D isolation',
    'ST_tex' : 'ST',
    'n_ak4_tex' : 'N(AK4 jets)',
    'n_ak8_tex' : 'N(AK8 jets)',
    'pt_ld_ak8_jet_tex' : 'p_T(1st AK8 jet)',
    'tot. eff._tex' : 'tot. eff.',
    'output/input_tex' : 'output/input',
    'TpTp_M-0700' : r'$\mathrm{T\bar{T}}$ (0.7 TeV)',
    'TpTp_M-0800' : r'$\mathrm{T\bar{T}}$ (0.8 TeV)',
    'TpTp_M-0900' : r'$\mathrm{T\bar{T}}$ (0.9 TeV)',
    'TpTp_M-1000' : r'$\mathrm{T\bar{T}}$ (1.0 TeV)',
    'TpTp_M-1100' : r'$\mathrm{T\bar{T}}$ (1.1 TeV)',
    'TpTp_M-1200' : r'$\mathrm{T\bar{T}}$ (1.2 TeV)',
    'TpTp_M-1300' : r'$\mathrm{T\bar{T}}$ (1.3 TeV)',
    'TpTp_M-1400' : r'$\mathrm{T\bar{T}}$ (1.4 TeV)',
    'TpTp_M-1500' : r'$\mathrm{T\bar{T}}$ (1.5 TeV)',
    'TpTp_M-1600' : r'$\mathrm{T\bar{T}}$ (1.6 TeV)',
    'TpTp_M-1700' : r'$\mathrm{T\bar{T}}$ (1.7 TeV)',
    'TpTp_M-1800' : r'$\mathrm{T\bar{T}}$ (1.8 TeV)',
    'BpBp_M-0700' : r'$\mathrm{B\bar{B}}$ (0.7 TeV)',
    'BpBp_M-0800' : r'$\mathrm{B\bar{B}}$ (0.8 TeV)',
    'BpBp_M-0900' : r'$\mathrm{B\bar{B}}$ (0.9 TeV)',
    'BpBp_M-1000' : r'$\mathrm{B\bar{B}}$ (1.0 TeV)',
    'BpBp_M-1100' : r'$\mathrm{B\bar{B}}$ (1.1 TeV)',
    'BpBp_M-1200' : r'$\mathrm{B\bar{B}}$ (1.2 TeV)',
    'BpBp_M-1300' : r'$\mathrm{B\bar{B}}$ (1.3 TeV)',
    'BpBp_M-1400' : r'$\mathrm{B\bar{B}}$ (1.4 TeV)',
    'BpBp_M-1500' : r'$\mathrm{B\bar{B}}$ (1.5 TeV)',
    'BpBp_M-1600' : r'$\mathrm{B\bar{B}}$ (1.6 TeV)',
    'BpBp_M-1700' : r'$\mathrm{B\bar{B}}$ (1.7 TeV)',
    'BpBp_M-1800' : r'$\mathrm{B\bar{B}}$ (1.8 TeV)',
    'TTbar' : r'$\mathrm{t\bar{t}}$',
    'DYJetsToLL' : 'DY + jets',
    'SingleTop' : 'Single top',
    'WJets' : 'W + jets',
    'ttbar_rate': 't#bar{t} rate',
    'qcd_rate': 'QCD rate',
    'wjets_rate': 'W+jets rate',
    'zjets_rate': 'Z+jets rate',
    'singlet_rate': 'Single t rate',
    'TTbar_rate': 't#bar{t} + jets rate',
    'QCD_rate': 'Multijet rate',
    'Diboson_rate': 'Diboson rate',
    'WJets_rate': 'W+jets rate',
    'DYJets_rate': 'Z+jets rate',
    'SingleTop_rate': 'Single t rate',
    'jec' : 'JES',
    'jer' : 'JER',
    'luminosity' : 'Luminosity',
    'btag_bc' : 'B tag: heavy fl.',
    'btag_udsg' : 'B tag: light fl.',
    'pu' : 'Pileup rew.',
    'sfmu_id' : 'ID: #mu',
    'sfmu_trg' : 'Trigger: #mu',
    'sfmu_iso' : 'Iso: #mu',
    'sfel_id' : 'ID: e',
    'sfel_trg' : 'Trigger: e',
    'sfel_iso' : 'Iso: e',
    'ScaleVar' : '#mu_{R/F} scale',
    'PDF' : 'PDF',
    'ttbar_scale' : 'PS scale',
    'PSScale' : 'PS scale',
    'top_pt_reweight' : 'top-p_{T} rew.',
    'ht_reweight' : 'H_{T}-rew.',
    'q2' : 'Top shower',
    'higgs_smear' : 'AK8 mass res.',
    'higgs_scale' : 'AK8 mass scale',
    'jmr' : 'Pruned mass resolution',
    'jms' : 'Pruned mass scale',
    'jsf' : 'H_{T}-rew.',
    'tau21' : 'W tagging: #tau_{2}/#tau_{1}',
    'taupt' : 'W tagging: #tau_{2}/#tau_{1} p_{T} dep.',
    'ScaleVarWJets' : '#mu_{RF} scales: W + jets',
    'ScaleVarTTbar' : '#mu_{RF} scales: t#bar{t} + jets',
    'ScaleVarSingleTop' : '#mu_{RF} scales: Single t',
    'ScaleVarQCD' : '#mu_{RF} scales: QCD',
    'ScaleVarDYJets' : '#mu_{RF} scales: Z + jets',
} )
# settings.defaults_Legend['x_pos'] = 0.80
# settings.defaults_Legend['label_width'] = 0.36
# settings.defaults_Legend['label_height'] = 0.04
# settings.debug_mode = True
# settings.box_text_size = 0.03
# settings.defaults_Legend['opt'] = 'f'
# settings.defaults_Legend['opt_data'] = 'p'
# settings.defaults_Legend['reverse'] = True

settings.stat_error_color = 923
settings.stat_error_fill = 3002
settings.sys_error_color = (632, 1.)
settings.sys_error_fill = 3002
settings.tot_error_color_main = (921, 0.6)
settings.tot_error_fill_main = 3644
settings.tot_error_color_bot = (921, 0.6)
settings.tot_error_fill_bot = 3644
settings.stack_line_color = None
settings.signal_linewidth = 2

def tot_error_style(histo, **kws):
    fill_color, fill_style = kws.get('tot_fill_color', settings.tot_error_color), kws.get('tot_fill_style', settings.tot_error_fill)
    kws.update({ 'fill_color' : fill_color, 'fill_style' : fill_style})
    histo.SetTitle(kws.get('tot_err_legend', 'Bkg. uncert.'))
    settings.apply_error_hist_style(histo, **kws)


def stat_error_style(histo, **kws):
    fill_color, fill_style = kws.get('stat_fill_color', settings.stat_error_color), kws.get('stat_fill_style', settings.stat_error_fill)
    kws.update({ 'fill_color' : fill_color, 'fill_style' : fill_style})
    histo.SetTitle(kws.get('stat_err_legend', 'Bkg. uncert. (stat.)'))
    settings.apply_error_hist_style(histo, **kws)

settings.tot_error_style = tot_error_style
settings.stat_error_style = stat_error_style

# Heiner's settings for total error:
# style = 3475
# color = ROOT.kGray+3

settings.defaults_BottomPlot['y_min'] = -0.9
settings.defaults_BottomPlot['y_max'] = 1.1
settings.defaults_BottomPlot['draw_opt'] = 'E0'
settings.defaults_BottomPlot['force_y_range'] = True
# settings.defaults_BottomPlot['poisson_errs'] = False

settings.__setattr__('legend_entries', [
    'Background',
    'nominal',
    'plus',
    'minus',
    # 'TTbar',
    # 'WJets',
    # 'ZJets',
    # 'DYJets',
    # 'DYJetsToLL',
    # 'SingleT',
    # 'SingleTop',
    # 'data',
    'Diboson',
    'QCD',
    'Data',
    'data',
    'T#bar{T}',
    't#bar{t}',
    'W + jets',
    'DY + jets',
    'Single t',
    'Stat. uncert. MC',
    'Sys. uncert. MC',
    'Tot. uncert. MC',
    '#pm 2 #sigma Expected ',
    '#pm 1 #sigma Expected ',
    '#pm 2 #sigma Observed ',
    '#pm 1 #sigma Observed ',
    ]
    )


def sort_legend_func(w):
    if 'Data' in w:
        ind = 0
    elif '0.8' in w:        
        ind = -1
    elif '1.2' in w:        
        ind = -2
    elif 'TeV' in w:
        ind = -3
    elif 'uncert' in w:
        ind = -999
    else:
        ind = -5
    return ind

# if settings.style != 'AN':
settings.defaults_Legend.update({
    'x_pos': 0.7,
    'y_pos': 0.66,
    'label_width': 0.30,
    'label_height': 0.040,
    'box_text_size' : 0.033,
    'opt': 'f',
    'opt_data': 'pl',
    'reverse': True,
    'sort_legend' : sort_legend_func,
    # 'clean_legend' : lambda w: any(a in w[1] for a in legend_entries),
})

settings.stacking_order = [
    'TTbar',
    'WJets',
    'SingleT',
    'SingleTop',
    'DYJets',
    'DYJetsToLL',
    'Diboson',
    'QCD',
]

settings.box_text_size = 0.033
# if settings.style != 'AN':
settings.canvas_size_x = 618
settings.canvas_size_y = 494
settings.root_style.SetPadTopMargin(0.125)
settings.root_style.SetPadBottomMargin(0.125)
settings.root_style.SetPadRightMargin(0.1)

settings.bottom_pad_height = 0.3




# def set_bottom_plot_general_style(obj):
#     obj.GetYaxis().CenterTitle(1)
#     obj.GetYaxis().SetTitleSize(0.15) #0.11
#     obj.GetYaxis().SetTitleOffset(0.44) #0.55
#     obj.GetYaxis().SetLabelSize(0.16)
#     obj.GetYaxis().SetNdivisions(205)
#     obj.GetXaxis().SetNoExponent()
#     obj.GetXaxis().SetTitleSize(0.16)
#     obj.GetXaxis().SetLabelSize(0.17)
#     obj.GetXaxis().SetTitleOffset(1)
#     obj.GetXaxis().SetLabelOffset(0.006)
#     obj.GetXaxis().SetNdivisions(505)
#     obj.GetXaxis().SetTickLength(obj.GetXaxis().GetTickLength() * 3.)
#     obj.SetTitle('')

def apply_split_pad_styles(cnv_wrp):
    main, scnd = cnv_wrp.main_pad, cnv_wrp.second_pad

    main.SetTopMargin(0.125)
    main.SetBottomMargin(settings.bottom_pad_height)
    #main.SetRightMargin(0.04)
    #main.SetLeftMargin(0.16)

    scnd.SetTopMargin(0.05)
    scnd.SetBottomMargin(0.375)
    #scnd.SetRightMargin(0.04)
    #scnd.SetLeftMargin(0.16)
    scnd.SetRightMargin(main.GetRightMargin())
    scnd.SetLeftMargin(main.GetLeftMargin())
    scnd.SetGridy()

    pars = [ctypes.c_double(), ctypes.c_double(), ctypes.c_double(), ctypes.c_double()]
    main.GetPadPar(*pars)
    pars = [d.value for d in pars]
    pars[1] += 0.002  # lift ylow very slightly
    main.SetPad(*pars)

    first_obj = cnv_wrp.first_obj
    first_obj.GetYaxis().CenterTitle(1)
    first_obj.GetYaxis().SetTitleSize(0.045)
    first_obj.GetYaxis().SetTitleOffset(1.4)
    first_obj.GetYaxis().SetLabelSize(0.055)
    first_obj.GetXaxis().SetNdivisions(505)

def set_bottom_plot_pull_style(obj):
    obj.SetFillColor(ROOT.kGray + 2)
    obj.SetLineColor(ROOT.kGray + 2)
    obj.GetYaxis().SetTitleSize(0.14) #0.11
    obj.GetYaxis().SetNdivisions(7) #0.11
    obj.GetYaxis().SetTitleOffset(0.3)
    obj.GetYaxis().SetLabelSize(0.16)

settings.apply_split_pad_styles = apply_split_pad_styles
settings.set_bottom_plot_pull_style = set_bottom_plot_pull_style

# from vlq_settings
# settings.colors = {
#     'TTbar': 632, # Red
#     'WJets': 902, # Pinkish
#     'ZJets': 840, # Blue
#     'ST': 434, # Orange
#     'QCD': 870,   # Light blue
# }
signals = {'TpTp_M-0800' : ROOT.kBlack,
    'TpTp_M-1200' : ROOT.kBlack,
    'TpTp_M-1600' : ROOT.kBlack
    }
final_states = final_states = ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']

for s, c in signals.iteritems():
    settings.colors.update(dict((s + f, c) for f in final_states))
    settings.colors.update({s+'_thX' : ROOT.kBlack, s+'_other' : ROOT.kBlack})



settings.colors.update({
    'Background' : 920,
    'nominal' : 1,
    'plus' : 2,
    'minus' : 3,
    'TTbar': 632-7,
    'WJets': 400-9,
    'ZJets': 432-9,
    'DYJets': 432-9,
    'DYJetsToLL': 432-9,
    'SingleT': 416-9,
    'SingleTop': 416-9,
    'Diboson' :616-9,
    'QCD': 851,
    'TpTp_M-0800' : ROOT.kBlack,
    'TpTp_M-1200' : ROOT.kBlack,
    'TpTp_M-0800_thX' : ROOT.kBlack,
    'TpTp_M-0800_other' : ROOT.kBlack,
    'TpTp_M-1200_thX' : ROOT.kBlack,
    'TpTp_M-1200_other' : ROOT.kBlack,
})
