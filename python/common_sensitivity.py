import varial.history

import varial.generators as gen
import varial.wrappers as wrappers

import UHH2.VLQSemiLepPreSel.common as vlq_common

import common_plot

theory_masses = [700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500.]
theory_cs = [0.455, 0.196, 0.090, 0.044, 0.022, 0.012, 0.006, 0.003, 0.002]


dict_factors_original = {
    'bwbw' : 0.111,
    'thth' : 0.111,
    'tztz' : 0.111,
    'thbw' : 0.222,
    'thtz' : 0.222,
    'tzbw' : 0.222
}

def make_factors_new(brs):
    dict_factors_new = {
        'bwbw' : brs['bw']*brs['bw'],
        'thth' : brs['th']*brs['th'],
        'tztz' : brs['tz']*brs['tz'],
        'thbw' : brs['th']*brs['bw']*2,
        'thtz' : brs['th']*brs['tz']*2,
        'tzbw' : brs['tz']*brs['bw']*2
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

def final_state_scaling(wrps, brs):
    dict_factors = make_finalstate_factors(make_factors_new(brs))
    for w in wrps:
        for final_state, factor in dict_factors.iteritems():
            if w.sample.endswith(final_state):
                w = scale_histo(w, factor)
        yield w

def set_category(wrps):
    for w in wrps:
        category = w.file_path.split('/')[-3]
        setattr(w, "category", category)
    return wrps

def loader_hook(wrps):
    wrps = vlq_common.add_wrp_info(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.in_file_path.split('/')[0])
    wrps = gen.sort(wrps, key_list=["category"])
    wrps = common_plot.merge_samples(wrps)
    wrps = vlq_common.label_axes(wrps)
    # wrps = final_state_scaling(wrps, dict_factors)
    return wrps

def loader_hook_scale(wrps, brs=None):
    if not brs:
        print 'WARNING: No branching ratios set, stop running!'
        return None
    wrps = loader_hook(wrps)
    wrps = final_state_scaling(wrps, brs)
    wrps = vlq_common.merge_decay_channels(wrps, (
        '_thbw',
        '_thth',
        '_thtz',
        '_noH_bwbw',
        '_noH_tzbw',
        '_noH_tztz'
        ))
    # wrps = list(wrps)
    # for w in wrps:
    #     print w.sample
    return wrps