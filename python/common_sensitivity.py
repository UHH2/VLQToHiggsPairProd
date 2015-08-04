import varial.history

import common_vlq
import varial.generators as gen
import varial.wrappers as wrappers

dict_factors_original = {
    'bwbw' : 0.2501776763,
    'thth' : 0.06163234751,
    'tztz' : 0.06168446588,
    'thbw' : 0.2502345327,
    'thtz' : 0.1252357172,
    'tzbw' : 0.2510352604
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
    wrps = common_vlq.add_wrp_info(wrps)
    # print wrps
    # wrps = set_category(wrps)
    wrps = varial.generators.gen_add_wrp_info(
        wrps, category=lambda w: w.file_path.split('/')[-3])
    wrps = gen.sort(wrps, key_list="category")
    wrps = common_vlq.merge_samples(wrps)
    # print "=====AFTER MERGING=====:"
    # for w in wrps:
    #     print "after:\n", w
    # wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)
    # wrps = final_state_scaling(wrps, dict_factors)
    return wrps

def loader_hook_scale(wrps, brs=None):
    if not brs:
        print 'WARNING: No branching ratios set, stop running!'
        return None
    wrps = loader_hook(wrps)
    wrps = final_state_scaling(wrps, brs)
    wrps = common_vlq.merge_decay_channels(wrps, (
        '_bwbw',
        '_thbw',
        '_thth',
        '_thtz',
        '_tzbw',
        '_tztz'
        ))
    return wrps