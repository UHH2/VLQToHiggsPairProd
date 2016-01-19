from ROOT import TGraph
from array import array
import glob
import os

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
        limit_rel_path='',
        plot_obs=False
    ):
        super(LimitGraphs, self).__init__(name)
        self.limit_rel_path = limit_rel_path
        self.plot_obs = plot_obs

    def make_graph(self, wrp, obs=False):
        x_arr = array('f', wrp.res_exp_x)
        y_arr = array('f', wrp.res_exp_y)
        lim_graph = TGraph(len(x_arr), x_arr, y_arr)
        if obs:
            lim_graph.SetLineStyle(8)
            lim_type='Obs'
        else:
            lim_type='Exp'
        selection = varial.settings.pretty_names[wrp.name]
        color = varial.settings.colors[wrp.name]
        lim_graph.SetLineColor(color)
        lim_graph.SetLineWidth(2)
        lim_graph.GetXaxis().SetTitle("m_{T'} [GeV]")
        lim_graph.GetYaxis().SetTitle("#sigma x BR [pb]")
        lim_wrapper = wrappers.GraphWrapper(lim_graph,
            legend=lim_type+' 95% CL '+selection,
            save_name='tH%.0ftZ%.0fbW%.0f' % (wrp.brs['th']*100, wrp.brs['tz']*100, wrp.brs['bw']*100),
            # selection=wrp.selection,
            # lim_type='exp',
            draw_option='L'
            )
        return lim_wrapper

    def run(self):
        # parents = os.listdir(self.cwd+'/..')
        theta_tools = glob.glob(os.path.join(self.cwd+'..', self.limit_rel_path))
        wrps = list(self.lookup_result(k) for k in theta_tools)
        # f = ROOT.TFile.Open(filename, "RECREATE")
        # f.cd()
        list_graphs=[]
        for w in wrps:
            list_graphs.append(self.make_graph(w))
            if self.plot_obs:
                list_graphs.append(self.make_graph(w, True))
        # tri_hist.Write()
        self.result = list_graphs
        # f.Close()


def add_th_curve(grps, th_x=None, th_y=None):
    for g in grps:
        x_arr=array('f', th_x)
        y_arr=array('f', th_y)
        th_graph = TGraph(len(x_arr), x_arr, y_arr)
        th_graph.SetLineStyle(9)
        th_graph.SetLineColor(1)
        th_graph.SetLineWidth(2)
        th_wrp = wrappers.GraphWrapper(th_graph,
                    legend='Theory',
                    draw_option='L'
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
