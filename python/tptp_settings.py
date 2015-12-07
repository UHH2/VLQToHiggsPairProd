from varial import settings
from varial.sample import Sample
import varial.analysis as analysis
import UHH2.VLQSemiLepPreSel.vlq_settings

settings.rootfile_postfixes = ['.root', '.png', '.pdf']

# settings.defaults_Legend['x_pos'] = 0.80
# settings.defaults_Legend['label_width'] = 0.36
# settings.defaults_Legend['label_height'] = 0.04
# settings.debug_mode = True
# settings.box_text_size = 0.03
# settings.defaults_Legend['opt'] = 'f'
# settings.defaults_Legend['opt_data'] = 'p'
# settings.defaults_Legend['reverse'] = True

# from vlq_settings
# settings.colors = {
#     'TTbar': 632, # Red
#     'WJets': 902, # Pinkish
#     'ZJets': 840, # Blue
#     'ST': 434, # Orange
#     'QCD': 870,   # Light blue
# }

settings.colors.update({
    # 'QCD' : 867,
    # 'TTbar': 632,
    # 'WJets': 878,
    # 'ZJets': 596,
    # 'TpTp_M-800_thX' : 800, # Yellow
    'TpTp_M-800_thX' : 634,
    'TpTp_M-800_other' : 616,
    # 'TpTp_M-1600_thX' : 797, # Orange
    'TpTp_M-1600_thX' : 418, # Green
    'TpTp_M-1600_other' : 593,
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
smpls = list()


smpls.append(Sample(
    name='MC_QCD',
    legend='MC_QCD'
))

smpls.append(Sample(
    name='MC_TTbar',
    legend='MC_TTbar'
))

smpls.append(Sample(
    name='MC_WJets',
    legend='MC_WJets'
))

smpls.append(Sample(
    name='MC_ZJets',
    legend='MC_ZJets'
))

smpls.append(Sample(
    name='MC_ST',
    legend='MC_ST'
))

analysis.all_samples = dict((s.name, s) for s in smpls)

settings.stacking_order = ['MC_ZJets', 'MC_WJets', 'MC_ST', 'MC_TTBar', 'MC_QCD']

# default_colors = [632, 814, 596, 870, 434, 840, 902, 797, 800, 891, 401, 800,
#                   838, 420, 403, 893, 881, 804, 599, 615, 831, 403, 593, 872]
