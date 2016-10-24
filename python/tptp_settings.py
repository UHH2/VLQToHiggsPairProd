from varial import settings
# from varial.sample import Sample
import varial.analysis as analysis
import UHH2.VLQSemiLepPreSel.vlq_settings
import ROOT

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
    'trigger_accept_el45_tex' : 'trigger',
    'trigger_accept_mu45_tex' : 'trigger',
    'primary_lepton_pt_tex' : 'p_T(Lepton)',
    'primary_electron_pt_tex' : 'p_T(Electron)',
    'primary_muon_pt_tex' : 'p_T(Muon)',
    'pt_ld_ak4_jet_tex' : 'p_T(1st AK4 jet)',
    'pt_subld_ak4_jet_tex' : 'p_T(2nd AK4 jet)',
    '2D cut_tex' : '2D cut',
    'ST_tex' : 'ST',
    'n_ak4_tex' : 'N(AK4 jets)',
    'n_ak8_tex' : 'N(AK8 jets)',
    'pt_ld_ak8_jet_tex' : 'p_T(1st AK8 jet)',
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
    'DYJetsToLL' : 'DY + jets',
    'SingleTop' : 'Single T',
    'WJets' : 'W + jets',
    'ttbar_rate': 'BH ttbar rate',
    'qcd_rate': 'BH qcd rate',
    'wjets_rate': 'BH w+jets rate',
    'zjets_rate': 'BH z+jets rate',
    'singlet_rate': 'single BH t rate',
    'TTbar_rate': 'BH ttbar rate',
    'QCD_rate': 'BH QCD rate',
    'Diboson_rate': 'BH Diboson rate',
    'WJets_rate': 'BH W+jets rate',
    'DYJets_rate': 'BH Z+jets rate',
    'SingleTop_rate': 'Single BH t rate',
    'jec' : 'JEC',
    'jer' : 'JER',
    'btag_bc' : 'btag eff.',
    'btag_udsg' : 'light flav. mistag',
    'pu' : 'pileup reweighting',
    'sfmu_id' : 'SF mu ID',
    'sfmu_trg' : 'SF mu trigger',
    'sfmu_iso' : 'SF mu isolation',
    'sfel_id' : 'SF el ID',
    'sfel_trg' : 'SF el trigger',
    'sfel_iso' : 'SF el isolation',
    'ScaleVar' : 'Q^{2} scale variations',
    'PDF' : 'PDF',
    'ttbar_scale' : 'PS scale variations',
    'PSScale' : 'PS scale variations',
    'top_pt_reweight' : 'top-p_{T} reweighting',
    'ht_reweight' : 'H_{T}-reweighting',
    'q2' : 'PS scale variations',
    'higgs_smear' : 'SD mass resolution',
    'jmr' : 'Pruned mass resolution',
    'jms' : 'Pruned mass scale',
    'jsf' : 'Bkg reweighting',
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
    'sort_legend' : lambda w: 'TT ' in w[1],
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

def apply_split_pad_styles(cnv_wrp):
    main, scnd = cnv_wrp.main_pad, cnv_wrp.second_pad

    main.SetTopMargin(0.1)
    main.SetBottomMargin(0.25)
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
    first_obj.GetYaxis().SetTitleSize(0.045)
    first_obj.GetYaxis().SetTitleOffset(1.3)
    first_obj.GetYaxis().SetLabelSize(0.055)
    first_obj.GetXaxis().SetNdivisions(505)

settings.apply_split_pad_styles = apply_split_pad_styles

# from vlq_settings
# settings.colors = {
#     'TTbar': 632, # Red
#     'WJets': 902, # Pinkish
#     'ZJets': 840, # Blue
#     'ST': 434, # Orange
#     'QCD': 870,   # Light blue
# }
signals = {'TpTp_M-800' : ROOT.kGreen,
    'TpTp_M-1200' : ROOT.kBlue,
    'TpTp_M-1600' : ROOT.kRed
    }
final_states = final_states = ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']

for s, c in signals.iteritems():
    settings.colors.update(dict((s + f, c) for f in final_states))
    settings.colors.update({s+'_thX' : ROOT.kAzure, s+'_other' : ROOT.kMagenta})



settings.colors.update({
    'Background' : 920,
    'nominal' : 1,
    'plus' : 2,
    'minus' : 3,
    'TTbar': 632 - 7,
    'WJets': 400-9,
    'ZJets': 432-9,
    'DYJets': 432-9,
    'DYJetsToLL': 432-9,
    'SingleT': 416-9,
    'SingleTop': 416-9,
    'Diboson' :616-9,
    'QCD': 851,
})
