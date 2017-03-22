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

def loader_hook_scale_excl(wrps, brs=None, merge=True):
    # if not brs:
    #     print 'WARNING: No branching ratios set, stop running!'
    #     return None
    wrps = loader_hook_excl(wrps)
    wrps = final_state_scaling(wrps, brs)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.category, w.sys_info, w.sample))
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    if merge:
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=True)
        wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=True)
    wrps = list(wrps)
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


######################################################### plot limit graphs ###
# class CompareLimitGraphs(varial.tools.Tool):

#     def __init__(self,
#         limit_path='',
#         hook_loaded_graphs=None,
#         group_graphs=lambda ws: gen.group(ws, key_func=lambda w: ''),
#         setup_graphs=None,
#         split_mass=False,
#         get_lim_params=None,
#         plot_obs=False,
#         plot_1sigmabands=False,
#         plot_2sigmabands=False,
#         axis_labels=('signal process', 'upper limit'),
#         name=None,
#     ):
#         super(LimitGraphsNew, self).__init__(name)
#         self.limit_path = limit_path
#         self.hook_loaded_graphs = hook_loaded_graphs
#         self.group_graphs = group_graphs
#         self.setup_graphs = setup_graphs
#         self.get_lim_params = self.get_lims_mass_split if split_mass else self.get_lims_mass_comb
#         if get_lim_params:
#             self.get_lim_params = get_lim_params
#         self.plot_obs = plot_obs
#         self.plot_1sigmabands = plot_1sigmabands
#         self.plot_2sigmabands = plot_2sigmabands
#         self.axis_labels = axis_labels

#     @staticmethod
#     def get_lims_mass_comb(grp):
#         wrp = grp[0]
#         theta_res_exp = cPickle.loads(wrp.res_exp)
#         theta_res_obs = cPickle.loads(wrp.res_obs)
#         if not theta_res_exp:
#             self.message('ERROR Theta result empty.')
#             raise RuntimeError  
#         x_list = theta_res_exp.x
#         y_exp_list = theta_res_exp.y
#         y_obs_list = theta_res_obs.y
#         sigma1_band_low = theta_res_exp.bands[1][0]
#         sigma2_band_low = theta_res_exp.bands[0][0]
#         sigma1_band_high = theta_res_exp.bands[1][1]
#         sigma2_band_high = theta_res_exp.bands[0][1]
#         return x_list, y_exp_list, y_obs_list, sigma1_band_low, sigma1_band_high, sigma2_band_low, sigma2_band_high

#     @staticmethod
#     def get_lims_mass_split(grp):
#         val_tup_list = []
#         wrps = grp.wrps
#         for wrp in wrps:
#             theta_res_exp = cPickle.loads(wrp.res_exp)
#             theta_res_obs = cPickle.loads(wrp.res_obs)
#             if not theta_res_exp:
#                 continue
#             x = theta_res_exp.x
#             y_exp = theta_res_exp.y
#             y_obs = theta_res_obs.y
#             sigma1_low = theta_res_exp.bands[1][0]
#             sigma2_low = theta_res_exp.bands[0][0]
#             sigma1_high = theta_res_exp.bands[1][1]
#             sigma2_high = theta_res_exp.bands[0][1]
#             if not (len(x)==1 and len(sigma1_low)==1 and len(sigma1_high)==1 and len(sigma2_low)==1 and len(sigma2_high)==1):
#                 monitor.message('limits.get_lims_mass_split', 'WARNING Not exactly one mass point in limit wrapper! ' +\
#                     'Length of x/sigma1_low/sigma1_high/sigma2_low/sigma2_high: %s/%s/%s/%s/%s' % (str(len(x)), str(len(sigma1_low)), str(len(sigma1_high)), str(len(sigma2_low)), str(len(sigma2_high))))
#             val_tup_list.append((x[0], y_exp[0], y_obs[0], sigma1_low[0], sigma2_low[0], sigma1_high[0], sigma2_high[0]))
#         val_tup_list = sorted(val_tup_list, key=lambda w: w[0])
#         x_list = list(w[0] for w in val_tup_list)
#         y_exp_list = list(w[1] for w in val_tup_list)
#         y_obs_list = list(w[2] for w in val_tup_list)
#         sigma1_band_low = list(w[3] for w in val_tup_list)
#         sigma2_band_low = list(w[4] for w in val_tup_list)
#         sigma1_band_high = list(w[5] for w in val_tup_list)
#         sigma2_band_high = list(w[6] for w in val_tup_list)
#         return x_list, y_exp_list, y_obs_list, sigma1_band_low, sigma1_band_high, sigma2_band_low, sigma2_band_high

#     def prepare_sigma_band_graph(self, x_list, sig_low, sig_high):
#         n_items = len(x_list)
#         sig_graph = ROOT.TGraph(2*n_items)
#         for i in xrange(0, n_items):
#             sig_graph.SetPoint(i, x_list[i], sig_low[i])
#         for i in xrange(0, n_items):
#             sig_graph.SetPoint(i+n_items, x_list[n_items-i-1],
#                 sig_high[n_items-i-1])
#         return sig_graph

#     def make_sigma_band_graph(self, x_list, sigma_band_low, sigma_band_high, sigma_ind, **kws):
#         assert type(sigma_ind) == int and (sigma_ind == 1 or sigma_ind == 2)
#         sigma_graph = self.prepare_sigma_band_graph(x_list, sigma_band_low,
#             sigma_band_high)
#         if sigma_ind == 1:
#             sigma_graph.SetFillColor(ROOT.kYellow)
#             legend='#pm 2 #sigma Expected'
#         else:
#             sigma_graph.SetFillColor(ROOT.kGreen)
#             legend='#pm 1 #sigma Expected'
#         sigma_graph.SetTitle(legend)
#         sigma_graph.GetXaxis().SetNdivisions(510, ROOT.kTRUE)

#         lim_wrapper = varial.wrappers.GraphWrapper(sigma_graph,
#             draw_option='F',
#             draw_option_legend='F',
#             val_y_min=min(sigma_band_low),
#             val_y_max=max(sigma_band_low)*10,
#             legend=legend,
#             save_name='lim_graph'
#         )
#         lim_wrapper.__dict__.update(kws)
#         return lim_wrapper

#     def make_graph(self, x_list, y_list, color, line_style, lim_type, **kws):
#         x_arr = array('f', x_list)
#         y_arr = array('f', y_list)
#         lim_graph = ROOT.TGraph(len(x_arr), x_arr, y_arr)
#         lim_graph.SetLineColor(color)
#         lim_graph.SetLineWidth(2)
#         lim_graph.SetLineStyle(line_style)
#         lim_graph.GetXaxis().SetNdivisions(510, ROOT.kTRUE)
#         lim_wrapper = varial.wrappers.GraphWrapper(lim_graph,
#             legend=lim_type+' 95% CL',
#             draw_option='L',
#             val_y_min=min(y_list),
#             val_y_max=max(y_list)*10,
#             save_name='lim_graph'
#         )
#         lim_wrapper.__dict__.update(kws)
#         return lim_wrapper

#     def run(self):
#         if self.limit_path.startswith('..'):
#             theta_tools = glob.glob(os.path.join(self.cwd, self.limit_path))
#         else:
#             theta_tools = glob.glob(self.limit_path)
#         wrps = list(self.lookup_result(k) for k in theta_tools)
#         if any(not a for a in wrps):
#             wrps = gen.dir_content(self.limit_path, '*.info', 'result')

#         if self.hook_loaded_graphs:
#             wrps = self.hook_loaded_graphs(wrps)

#         if self.group_graphs:
#             wrps = self.group_graphs(wrps)

#         if self.setup_graphs:
#             wrps = self.setup_graphs(wrps)

#         list_graphs=[]
#         for w in wrps:
#             x_list, y_exp_list, y_obs_list, sigma1_band_low, sigma1_band_high, sigma2_band_low, sigma2_band_high = self.get_lim_params(w)
#             args = w.__dict__
#             for i in ['wrps', 'name', 'type', 'klass', 'title']:
#                 args.pop(i, None)
#             if self.plot_2sigmabands:
#                 list_graphs.append(self.make_sigma_band_graph(x_list, sigma2_band_low, sigma2_band_high, 1, **args))
#             if self.plot_1sigmabands:
#                 list_graphs.append(self.make_sigma_band_graph(x_list, sigma1_band_low, sigma1_band_high, 2, **args))
#             list_graphs.append(self.make_graph(x_list, y_exp_list, ROOT.kBlack, 3, 'Expected', **args))
#             if self.plot_obs:
#                 list_graphs.append(self.make_graph(x_list, y_obs_list, ROOT.kBlack, 1, 'Observed', **args))

#         list_graphs[0].draw_option += 'A'

#         for l in list_graphs:
#             x_title, y_title = self.axis_labels
#             l.obj.GetXaxis().SetTitle(x_title)
#             l.obj.GetYaxis().SetTitle(y_title)

#         self.result = varial.wrp.WrapperWrapper(list_graphs)