from ROOT import TGraph, TGraphAsymmErrors, TMultiGraph
from array import array

import glob
import os
import cPickle
import theta_auto

import varial.settings
import varial.tools
import varial.wrappers as wrappers
import varial.util as util

from UHH2.VLQSemiLepPreSel.common import TpTpThetaLimits

# colors = {  "" : 2,
#             "loose" : 2,
#             "med" : 3,
#             "MedNoCat" : 3,
#             "MedCat" : 4}

# class TpTpLimitsWithProperties(TpTpThetaLimits):
#     def __init__(self, selection, color, *args ,**kws):
#         super(TpTpLimitsWithProperties, self).__init__(*args, **kws)
#         self.selection = selection
#         self.color = color

#     def run(self):
#         super(TpTpLimitsWithProperties, self).run()
#         self.result

class LimitGraphs(varial.tools.Tool):
    def __init__(self,
        name=None,
        limit_path='',
        plot_obs=False,
        plot_1sigmabands=False,
        plot_2sigmabands=False,
    ):
        super(LimitGraphs, self).__init__(name)
        self.limit_path = limit_path
        self.plot_obs = plot_obs
        self.plot_1sigmabands = plot_1sigmabands
        self.plot_2sigmabands = plot_2sigmabands

    def make_sigma_band_graph(self, theta_res, sigma_ind=1):
        assert(type(sigma_ind) == int and (sigma_ind == 0 or sigma_ind == 1))
        zero_array = array('f', [0] * len(theta_res.x))
        x_arr = array('f', theta_res.x)
        y_arr = array('f', theta_res.y)
        sigma_band_low = array('f', list(theta_res.y[ind]-err for ind, err in enumerate(theta_res.bands[sigma_ind][0])))
        sigma_band_high = array('f', list(err - theta_res.y[ind] for ind, err in enumerate(theta_res.bands[sigma_ind][1])))
        # print theta_res.y, sigma_band_low, sigma_band_high
        sigma_graph = TGraphAsymmErrors(len(x_arr), x_arr, y_arr,
            zero_array, zero_array, sigma_band_low, sigma_band_high)
        if sigma_ind == 1:
            sigma_graph.SetFillColor(3)
        else:
            sigma_graph.SetFillColor(5)
        setattr(sigma_graph, 'draw_option', '3')
        setattr(sigma_graph, 'y_min', min(theta_res.bands[sigma_ind][0]))
        setattr(sigma_graph, 'y_max', max(theta_res.bands[sigma_ind][1]))
        return sigma_graph

    def make_graph(self, theta_res, color):
        x_arr = array('f', theta_res.x)
        y_arr = array('f', theta_res.y)
        lim_graph = TGraph(len(x_arr), x_arr, y_arr)
        lim_graph.SetLineColor(color)
        lim_graph.SetLineWidth(2)
        lim_graph.GetXaxis().SetTitle("m_{T'} [GeV]")
        lim_graph.GetYaxis().SetTitle("#sigma x BR [pb]")
        return lim_graph

    def make_multi_graph(self, wrp):
        theta_res_exp = cPickle.loads(wrp.res_exp)
        color = varial.settings.colors[wrp.name]
        lim_graph_exp = self.make_graph(theta_res_exp, color)
        if self.plot_obs:
            theta_res_obs = cPickle.loads(wrp.res_obs)
            lim_graph_obs = self.make_graph(theta_res_obs, color)
        selection = varial.settings.pretty_names[wrp.name]
        x_min = lim_graph_exp.GetXaxis().GetXmin()
        x_max = lim_graph_exp.GetXaxis().GetXmax()
        y_min = lim_graph_exp.GetYaxis().GetXmin()
        y_max = lim_graph_exp.GetYaxis().GetXmax()
        if self.plot_obs:
            x_min = min(x_min, lim_graph_obs.GetXaxis().GetXmin())
            x_max = max(x_max, lim_graph_obs.GetXaxis().GetXmax())
            y_min = min(y_min, lim_graph_obs.GetYaxis().GetXmin())
            y_max = max(y_max, lim_graph_obs.GetYaxis().GetXmax())
        lim_graph_exp.SetLineStyle(3)
        # lim_type='Exp'
        if self.plot_obs:
            lim_graph_obs.SetLineStyle(1)
            # lim_type='Obs'
        onesigma_band = None
        twosigma_band = None
        if self.plot_1sigmabands:
            onesigma_band = self.make_sigma_band_graph(theta_res_exp, 1)
        if self.plot_2sigmabands:
            twosigma_band = self.make_sigma_band_graph(theta_res_exp, 0)
        all_graphs = TMultiGraph()
        if twosigma_band:
            all_graphs.Add(twosigma_band, twosigma_band.draw_option)
            y_min = twosigma_band.y_min
            y_max = twosigma_band.y_max
        if onesigma_band:
            all_graphs.Add(onesigma_band, onesigma_band.draw_option)
            if not twosigma_band:
                y_min = onesigma_band.y_min
                y_max = onesigma_band.y_max
        all_graphs.Add(lim_graph_exp, 'L')
        if self.plot_obs:
            all_graphs.Add(lim_graph_obs, 'L')
        # print 'next graph'
        # all_graphs.Draw('a')
        # print all_graphs.GetXaxis()       
        # print all_graphs.GetHistogram()       
        lim_wrapper = wrappers.MultiGraphWrapper(all_graphs,
            # legend=lim_type+' 95% CL '+selection,
            save_name='tH%.0ftZ%.0fbW%.0f' % (wrp.brs['th']*100, wrp.brs['tz']*100, wrp.brs['bw']*100),
            # selection=wrp.selection,
            # lim_type='exp',
            draw_option='',
            val_x_min = x_min,
            val_x_max = x_max,
            val_y_min = y_min,
            val_y_max = y_max,
            )
        return lim_wrapper

    def run(self):
        # parents = os.listdir(self.cwd+'/..')
        if self.limit_path.startswith('..'):
            theta_tools = glob.glob(os.path.join(self.cwd, self.limit_path))
        else: 
            theta_tools = glob.glob(self.limit_path)
        wrps = list(self.lookup_result(k) for k in theta_tools)
        # f = ROOT.TFile.Open(filename, "RECREATE")
        # f.cd()
        list_graphs=[]
        for w in wrps:
            list_graphs.append(self.make_multi_graph(w))
            # if self.plot_obs:
            #     list_graphs.append(self.make_graph(w, True))
        # tri_hist.Write()
        self.result = list_graphs
        # f.Close()


def add_th_curve(grps, th_x=None, th_y=None):
    for g in grps:
        x_arr=array('f', th_x)
        y_arr=array('f', th_y)
        th_graph = TGraph(len(x_arr), x_arr, y_arr)
        th_graph.SetLineStyle(2)
        th_graph.SetLineColor(1)
        th_graph.SetLineWidth(2)
        th_wrp = wrappers.GraphWrapper(th_graph,
                    legend='Theory',
                    draw_option='C'
                    )
        g = list(g)
        g.append(th_wrp)
        yield wrappers.WrapperWrapper(g, save_name=g[0].save_name)


# class TheoryCurve(util.Decorator):

#     def __init__(self, th_x=None, th_y=None, **kws):
#         super(TheoryCurve, self).__init__(**kws)
#         self.theory_x = th_x
#         self.theory_y = th_y

#     def draw_full_plot(self):
#         self.decoratee.draw_full_plot()
#         x_arr=array('f', self.theory_x)
#         y_arr=array('f', self.theory_y)
#         th_graph = TGraph(len(x_arr), x_arr, y_arr)
#         th_graph.SetLineStyle(7)
#         th_graph.SetLineColor(1)
#         th_graph.Draw('L')
