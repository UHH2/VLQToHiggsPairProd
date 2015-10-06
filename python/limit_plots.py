from ROOT import TGraph
from array import array
import glob
import os

import varial.tools
import varial.wrappers as wrappers
import varial.util as util

class LimitGraphs(varial.tools.Tool):
    def __init__(self,
        name=None,
        limit_rel_path=''
    ):
        super(LimitGraphs, self).__init__(name)
        self.limit_rel_path = limit_rel_path


    def run(self):
        # parents = os.listdir(self.cwd+'/..')
        theta_tools = glob.glob(os.path.join(self.cwd+'..', self.limit_rel_path))
        wrps = list(self.lookup_result(k) for k in theta_tools)
        # f = ROOT.TFile.Open(filename, "RECREATE")
        # f.cd()
        list_graphs=[]
        for w in wrps:
            x_arr = array('f', w.res_exp_x)
            y_arr = array('f', w.res_exp_y)
            lim_graph = TGraph(len(x_arr), x_arr, y_arr)
            lim_graph.SetLineColor(2)
            lim_graph.SetLineWidth(2)
            lim_graph.GetXaxis().SetTitle("T' mass [GeV]")
            lim_graph.GetYaxis().SetTitle("CS upper limit [pb]")
            list_graphs.append(wrappers.GraphWrapper(lim_graph,
                legend='tH:%.1f tZ:%.1f bW:%.1f' % (w.brs['th'], w.brs['tz'], w.brs['bw']),
                save_name='tH%.0ftZ%.0fbW%.0f' % (w.brs['th']*100, w.brs['tz']*100, w.brs['bw']*100),
                draw_option='L'
                ))
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
