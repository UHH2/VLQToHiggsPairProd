import varial.history

import varial.generators as gen
import varial.wrappers as wrappers

import UHH2.VLQSemiLepPreSel.common as vlq_common

import common_plot_new as common_plot
from varial.extensions.limits import *

theory_masses = [700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800]
theory_cs = [0.455, 0.196, 0.0903, 0.0440, 0.0224, 0.0118, 0.00639, 0.00354, 0.00200, 0.001148, 0.000666, 0.000391]


# Limit0 -> tH: 100%, tZ: 0%, bW: 0%
# Limit1 -> tH: 80%, tZ: 20%, bW: 0%
# Limit2 -> tH: 60%, tZ: 40%, bW: 0%
# Limit3 -> tH: 40%, tZ: 60%, bW: 0%
# Limit4 -> tH: 20%, tZ: 80%, bW: 0%
# Limit5 -> tH: 0%, tZ: 100%, bW: 0%
# Limit6 -> tH: 80%, tZ: 0%, bW: 20%
# Limit7 -> tH: 60%, tZ: 20%, bW: 20%
# Limit8 -> tH: 40%, tZ: 40%, bW: 20%
# Limit9 -> tH: 20%, tZ: 60%, bW: 20%
# Limit10 -> tH: 0%, tZ: 80%, bW: 20%
# Limit11 -> tH: 60%, tZ: 0%, bW: 40%
# Limit12 -> tH: 40%, tZ: 20%, bW: 40%
# Limit13 -> tH: 20%, tZ: 40%, bW: 40%
# Limit14 -> tH: 0%, tZ: 60%, bW: 40%
# Limit15 -> tH: 40%, tZ: 0%, bW: 60%
# Limit16 -> tH: 20%, tZ: 20%, bW: 60%
# Limit17 -> tH: 0%, tZ: 40%, bW: 60%
# Limit18 -> tH: 20%, tZ: 0%, bW: 80%
# Limit19 -> tH: 0%, tZ: 20%, bW: 80%
# Limit20 -> tH: 0%, tZ: 0%, bW: 100%

final_states = [
    'bwbw',
    'thth',
    'tztz',
    'thbw',
    'thtz',
    'tzbw'
]

dict_factors_original = {
    'bwbw' : 0.111,
    'thth' : 0.111,
    'tztz' : 0.111,
    'thbw' : 0.222,
    'thtz' : 0.222,
    'tzbw' : 0.222,
    'twtw' : 0.111,
    'bhbh' : 0.111,
    'bzbz' : 0.111,
    'bhtw' : 0.222,
    'bhbz' : 0.222,
    'bztw' : 0.222
}

def make_factors_new(brs):
    dict_factors_new = {
        'bwbw' : brs['w']*brs['w'],
        'thth' : brs['h']*brs['h'],
        'tztz' : brs['z']*brs['z'],
        'thbw' : brs['h']*brs['w']*2,
        'thtz' : brs['h']*brs['z']*2,
        'tzbw' : brs['z']*brs['w']*2,
        'twtw' : brs['w']*brs['w'],
        'bhbh' : brs['h']*brs['h'],
        'bzbz' : brs['z']*brs['z'],
        'bhtw' : brs['h']*brs['w']*2,
        'bhbz' : brs['h']*brs['z']*2,
        'bztw' : brs['z']*brs['w']*2
    }
    return dict_factors_new


def make_finalstate_factors(dict_factors_new):
    dict_factors = {}
    for final_state in dict_factors_new.iterkeys():
        dict_factors[final_state] = dict_factors_new[final_state]/dict_factors_original[final_state]
    return dict_factors


@varial.history.track_history
def scale_histo(wrp, factor=1.):
    histo = wrp.histo.Clone()
    histo.Scale(factor)
    info = wrp.all_info()
    info["lumi"] = 1.
    return wrappers.HistoWrapper(histo, **info)

def final_state_scaling(wrps, brs=None):
    if brs:
        dict_factors = make_finalstate_factors(make_factors_new(brs))
        for w in wrps:
            for final_state, factor in dict_factors.iteritems():
                if hasattr(w, 'finalstate'):
                    if w.finalstate == final_state:
                        w = scale_histo(w, factor)
                else:
                    if w.sample.endswith(final_state):
                        w = scale_histo(w, factor)
            yield w
    else:
        for w in wrps: yield w

# def set_category(wrps):
#     for w in wrps:
#         category = w.file_path.split('/')[-3]
#         setattr(w, "category", category)
#     return wrps

def get_final_state(wrp):
    if any(wrp.sample.endswith(g) for g in ['thth', 'thtz', 'thbw']):
        return wrp.sample[-4:]
    elif any(wrp.sample.endswith(g) for g in ['noH_tztz', 'noH_tzbw', 'noH_bwbw']):
        return wrp.sample[-8:]
    else: return ''

def subtract_finalstate(wrp):
    if not wrp.finalstate:
        return wrp.sample
    else:
        return wrp.sample[:-(len(wrp.finalstate)+1)]

def loader_hook_excl(wrps):
    wrps = common_plot.add_wrp_info(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.in_file_path.split('/')[0])
    # wrps = gen.gen_add_wrp_info(
    #     wrps,
    #     finalstate = get_final_state,
    #     # variable=lambda w: w.in_file_path.split('/')[-1]
    #     )
    # wrps = gen.gen_add_wrp_info(
    #     wrps,
    #     sample = subtract_finalstate,
    #     # variable=lambda w: w.in_file_path.split('/')[-1]
    #     )
    # wrps = common_plot.merge_samples(wrps)
    wrps = vlq_common.label_axes(wrps)
    # wrps = final_state_scaling(wrps, dict_factors)
    return wrps

def loader_hook_scale_excl(wrps, brs=None):
    # if not brs:
    #     print 'WARNING: No branching ratios set, stop running!'
    #     return None
    wrps = loader_hook_excl(wrps)
    wrps = final_state_scaling(wrps, brs)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.category, w.sys_info, w.sample))
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.category, w.sys_info,  w.sample
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=True)
    wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=True)
    # wrps = common_plot.merge_finalstates_channels(wrps, [
    #     'thbw',
    #     'thth',
    #     'thtz',
    #     'noH_bwbw',
    #     'noH_tzbw',
    #     'noH_tztz'
    #     ], print_warning=False
    #     )
    wrps = gen.sort(wrps, key_list=["category"])
    return wrps


class TpTpThetaLimits(ThetaLimits):
    def __init__(self, brs=None, *args ,**kws):
        super(TpTpThetaLimits, self).__init__(*args, **kws)
        self.brs = brs

    def run(self):
        super(TpTpThetaLimits, self).run()
        self.result.__dict__.update({
            'brs' : self.brs,
            # 'masses' : list(int(x) for x in self.result.res_exp_x)
            }
        )


class TpTpThetaLimitsFromFile(ThetaLimitsFromFile):
    def __init__(self, brs=None, *args ,**kws):
        super(TpTpThetaLimitsFromFile, self).__init__(*args, **kws)
        self.brs = brs

    def run(self):
        super(TpTpThetaLimitsFromFile, self).run()
        self.result.__dict__.update({
            'brs' : self.brs,
            # 'masses' : list(int(x) for x in self.result.res_exp_x)
            }
        )