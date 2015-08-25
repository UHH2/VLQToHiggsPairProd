from varial import settings
from varial.sample import Sample
import varial.analysis as analysis

settings.rootfile_postfixes = ['.root', '.png', '.pdf']

settings.defaults_Legend['x_pos'] = 0.80
settings.defaults_Legend['label_width'] = 0.36
settings.defaults_Legend['label_height'] = 0.04
# settings.debug_mode = True
settings.box_text_size = 0.03
settings.colors = {
    'QCD' : 867,
    'TTbar': 632,
    'WJets': 878,
    'ZJets': 596,
    # 'TpTp_M800': 416,
    # 'TpTp_M1000_thth': 800,
    # 'TpTp_M1000_thtz': 400,
    # 'TpTp_M1000_thbw': 616,
    # 'TpTp_M1000_tztz': 797,
    # 'TpTp_M1000_tzbw': 902,
    # 'TpTp_M1000_bwbw': 593,
}

# sample definitions
smpls = list()


smpls.append(Sample(
    name='QCD',
    legend='QCD'
))

smpls.append(Sample(
    name='TTbar',
    legend='TTbar'
))

smpls.append(Sample(
    name='WJets',
    legend='WJets'
))

smpls.append(Sample(
    name='ZJets',
    legend='ZJets'
))

smpls.append(Sample(
    name='SingleT',
    legend='SingleT'
))

# smpls.append(Sample(
#     name='TpTp_M-800',
#     legend='TpTp_M800'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_thth',
#     legend='TpTp_M1000_thth'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_thtz',
#     legend='TpTp_M1000_thtz'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_thbw',
#     legend='TpTp_M1000_thbw'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_tztz',
#     legend='TpTp_M1000_tztz'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_tzbw',
#     legend='TpTp_M1000_tzbw'
# ))

# smpls.append(Sample(
#     name='TpTp_M1000_bwbw',
#     legend='TpTp_M1000_bwbw'
# ))

analysis.all_samples = dict((s.name, s) for s in smpls)

settings.stacking_order = ['ZJets', 'WJets', 'SingleTop', 'TTBar', 'QCD']

# default_colors = [632, 814, 596, 870, 434, 840, 902, 797, 800, 891, 401, 800,
#                   838, 420, 403, 893, 881, 804, 599, 615, 831, 403, 593, 872]