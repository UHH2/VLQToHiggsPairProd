from varial import settings
from varial.sample import Sample
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
settings.__setattr__('lookup_aliases', True)
settings.__setattr__('style', 'PAS')

settings.cutflow_precision.update({
    'TpTp_M-0700' : "%17.1f",
    'TpTp_M-1000' : "%17.1f",
    'TpTp_M-1300' : "%17.2f",
    'TpTp_M-1700' : "%17.3f",
    })
# settings.defaults_Legend['x_pos'] = 0.80
# settings.defaults_Legend['label_width'] = 0.36
# settings.defaults_Legend['label_height'] = 0.04
# settings.debug_mode = True
# settings.box_text_size = 0.03
# settings.defaults_Legend['opt'] = 'f'
# settings.defaults_Legend['opt_data'] = 'p'
# settings.defaults_Legend['reverse'] = True

settings.sys_error_color = (632, 1.)
settings.sys_error_fill = 3002
settings.tot_error_color = (923, 1.)
settings.tot_error_fill = 3002

settings.defaults_BottomPlot['y_min'] = -2.
settings.defaults_BottomPlot['y_max'] = 2.
# settings.defaults_BottomPlot['force_y_range'] = True
# settings.defaults_BottomPlot['poisson_errs'] = False

if settings.style != 'AN':
    settings.defaults_Legend.update({
        'x_pos': 0.7,
        'y_pos': 0.72,
        'label_width': 0.3,
        'label_height': 0.035,
        'opt': 'f',
        'opt_data': 'p',
        'reverse': True,
    })

settings.defaults_Legend.update({
        'sort_legend' : lambda w: 'TT ' in w[1]
    })

settings.stacking_order = [
    'TTbar',
    'WJets',
    'SingleT',
    'DYJets',
    'QCD',
]

settings.box_text_size = 0.03
if settings.style != 'AN':
    settings.canvas_size_x = 618
    settings.canvas_size_y = 494
    settings.root_style.SetPadTopMargin(0.125)
    settings.root_style.SetPadBottomMargin(0.125)
    settings.root_style.SetPadRightMargin(0.1)

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
    settings.colors.update({s+'_thX' : ROOT.kOrange, s+'_other' : ROOT.kAzure})



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
    'QCD': 851,
    # 'QCD' : 867,
    # 'TTbar': 632,
    # 'WJets': 878,
    # 'ZJets': 596,
    # 'TpTp_M-800_thX' : 800, # Yellow
    # 'TpTp_M-800_thX' : 634,
    # 'TpTp_M-800_other' : 616,
    # # 'TpTp_M-1600_thX' : 797, # Orange
    # 'TpTp_M-1600_thX' : 418, # Green
    # 'TpTp_M-1600_other' : 593,
    # 'TpTp_M800': 416,
    # 'TpTp_M1000_thth': 800,
    # 'TpTp_M1000_thtz': 400,   # Yellow
    # 'TpTp_M1000_thbw': 616,
    # 'TpTp_M1000_tztz': 797,
    # 'TpTp_M1000_tzbw': 902,
    # 'TpTp_M1000_bwbw': 593,
})

# settings.max_open_root_files = 100
# settings.max_num_processes = 20

# sample definitions
# smpls = list()


# smpls.append(Sample(
#     name='QCD',
#     legend='QCD'
# ))

# smpls.append(Sample(
#     name='TTbar',
#     legend='TTbar'
# ))

# smpls.append(Sample(
#     name='WJets',
#     legend='WJets'
# ))

# smpls.append(Sample(
#     name='DYJetsToLL',
#     legend='DYJetsToLL'
# ))

# smpls.append(Sample(
#     name='SingleTop',
#     legend='SingleTop'
# ))

# analysis.all_samples = dict((s.name, s) for s in smpls)

settings.stacking_order = ['TTBar', 'WJets', 'SingleT', 'SingleTop', 'DYJets', 'DYJetsToLL', 'QCD']

# default_colors = [632, 814, 596, 870, 434, 840, 902, 797, 800, 891, 401, 800,
#                   838, 420, 403, 893, 881, 804, 599, 615, 831, 403, 593, 872]
