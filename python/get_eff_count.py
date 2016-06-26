from math import sqrt, floor, log10
import UHH2.VLQSemiLepPreSel.common as common
import varial.plotter
import varial.tools
import cPickle
import array
import ROOT
import itertools
import os
import pprint
import collections
from math import sqrt

order_cats = ['Preselection', '0H category', 'H1B category', 'H2B category']
order_smpls = [
    'TT M0700 incl.', 'TT M0900 incl.', 'TT M1100 incl.', 'TT M1300 incl.', 'TT M1500 incl.', 'TT M1700 incl.',
    'TT M0700 tHtH', 'TT M0900 tHtH', 'TT M1100 tHtH', 'TT M1300 tHtH', 'TT M1500 tHtH', 'TT M1700 tHtH'
    ]

count_prec = {
    'TT M0700' : "%.2f",
    'TT M1000' : "%.3f",
    'TT M1300' : "%.4f",
    'TT M1700' : "%.4f",
    # 'TTbar' : "%.1f",
    # 'WJets' : "%.1f",
    # 'DYJets' : "%.1f",
    # 'QCD' : "%.1f",
    # 'SingleTop' : "%.1f",
    r'\textbf{data}' : "%d"

    }

eff_prec = {
    'TT M0700' : "%.2f",
    'TT M1000' : "%.2f",
    'TT M1300' : "%.2f",
    'TT M1700' : "%.2f",
    'TTbar' : "%.3f",
    # 'WJets' : "%.1f",
    # 'DYJets' : "%.1f",
    # 'QCD' : "%.1f",
    # 'SingleTop' : "%.1f",
    # r'\textbf{data}' : "%d"

    }

def sort_cats(sort_list):
    def tmp(tpl):

        def comparable_str(s):
            # reverse...
            pos = sort_list.index(s)
            # need comparable string that sorts before alpha chars
            return str(pos * 0.001)
        return (comparable_str(tpl[0]) if tpl[0] in sort_list else '_')
    return tmp





class NumTableNew(varial.tools.Tool):
    def __init__(self, input_blocks, get_region, squash_errs=False, name=None):
        super(NumTableNew, self).__init__(name)
        self.input_blocks = input_blocks
        self.regions = get_region
        self.squash_errs = squash_errs

    def get_precision(self, num):
        if num >= 1.0:
            return "{0:17.1f}"
        elif num > 0:
            ex_dim = abs(floor(log10(num)))
            add_prec = 0
            if num*10**ex_dim < 2.:
                add_prec = 1
            prec = int(ex_dim+add_prec)
            prec = "{0:17."+str(prec)+"f}"
            return prec
        else:
            return "{0:17.0f}"

    def create_block(self, sample_dict):
        pass
        

    def run(self):
        
        self.regions = list((r, f(self.cwd)) for r, f in self.regions)
        self.regions = sorted(self.regions, key=sort_cats(order_cats))

        lines = []
        lines.append(r"\begin{tabular}{|l "
            + len(self.regions)*"| r "
            + r"|}\hline")
        lines.append("process & " + r" & ".join(r for r, _ in self.regions)
            + r"\\ \hline")
        # if not self.calc_eff:
        for smpl_dict in self.input_blocks:
            smpl_dict = sorted(smpl_dict, key=sort_cats(order_smpls))
            lines += self.create_block(smpl_dict)
            lines.append(r"\hline")
        
        lines.append(r"\end{tabular}")

        lines = '\n'.join(lines)
        with open(self.cwd+'count_table_content.tex', 'w') as f:
            f.write(lines)


class EffTable(NumTableNew):
    def __init__(self, input_blocks, get_region, norm_fct, squash_errs=False, name=None):
        super(EffTable, self).__init__(input_blocks, get_region, squash_errs, name)
        self.norm_fct = norm_fct

    def create_block(self, sample_dict):

        lines = []
        for sample_tup in sample_dict:
            try:
                s, s_func, sym_errs = sample_tup
            except ValueError:
                s, s_func = sample_tup
                sym_errs = False
            # filt_smpls = list(itertools.ifilter(fs, res))
            line = s + " "
            if isinstance(self.norm_fct, list):
                for smpl, fct in self.norm_fct:
                    if smpl in s:
                        baseline_count = fct
            else:
                baseline_count = self.norm_fct
            baseline_count = baseline_count/100.
            for r, r_dict in self.regions:
                line += "&$ "
                info = None
                # info = list(itertools.ifilter(s_func, r_dict))
                # if len(info) != 1:
                #     self.message('WARNING! Not exactly one key word found for sample {0} and region {1}'.format(s, r))
                # info = info[0][]
                for key, val in r_dict.iteritems():
                    if s_func(key):
                        info = val
                # info = self.get_info(r, s, filt_smpls, fr, res, key_word)
                if not info:
                    self.message('WARNING! No key word found for sample {0} and region {1}'.format(s, r))
                    continue
                if 'data' in s:
                    prec = "{0:17.0f}"
                else:
                    prec = self.get_precision(info[1]/baseline_count)
                if self.squash_errs:
                    stat_err = info[1]
                    syst_err = max(abs(info[2]), abs(info[3])) if len(info) == 4 else 0.
                    tot_err = sqrt(stat_err**2+syst_err**2)
                    line += prec.format(info[0]/baseline_count)
                    if 'data' not in s:
                        line += r" \% \pm " + prec.format(tot_err/baseline_count) + r" \%"
                elif sym_errs:
                    line += prec.format(info[0]/baseline_count)
                    if 'data' not in s:
                        line += r" \% \pm " + prec.format(info[1]/baseline_count) + r" \%"
                    if len(info) == 4:
                        syst_err = max(abs(info[2]), abs(info[3]))
                        line += r" \pm " + prec.format(syst_err/baseline_count)
                else:
                    line += prec.format(info[0]/baseline_count)
                    if 'data' not in s:
                        line += r" \% \pm " + prec.format(info[1]/baseline_count) + r" \%"
                    if len(info) == 4:
                        line += "^{+"+prec.format(info[2]/baseline_count)+r" \%}_{"+prec.format(info[3]/baseline_count)+r" \%}"
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines

class CountTable(NumTableNew):
    def __init__(self, input_blocks, get_region, squash_errs=False, name=None):
        super(CountTable, self).__init__(input_blocks, get_region, squash_errs, name)

    def create_block(self, sample_dict):

        lines = []
        for sample_tup in sample_dict:
            try:
                s, s_func, sym_errs = sample_tup
            except ValueError:
                s, s_func = sample_tup
                sym_errs = False
            # filt_smpls = list(itertools.ifilter(fs, res))
            line = s + " "
            for r, r_dict in self.regions:
                line += "&$ "
                info = None
                for key, val in r_dict.iteritems():
                    if s_func(key):
                        info = val
                # info = self.get_info(r, s, filt_smpls, fr, res, key_word)
                if not info:
                    self.message('WARNING! No key word found for sample {0} and region {1}'.format(s, r))
                    continue
                if 'data' in s:
                    prec = "{0:17.0f}"
                else:
                    prec = self.get_precision(info[1])
                if self.squash_errs:
                    stat_err = info[1]
                    syst_err = max(abs(info[2]), abs(info[3])) if len(info) == 4 else 0.
                    tot_err = sqrt(stat_err**2+syst_err**2)
                    line += prec.format(info[0])
                    if 'data' not in s:
                        line += r" \pm " + prec.format(tot_err)
                elif sym_errs:
                    line += prec.format(info[0])
                    if 'data' not in s:
                        line += r" \pm " + prec.format(info[1])
                    if len(info) == 4:
                        syst_err = max(abs(info[2]), abs(info[3]))
                        line += r" \pm " + prec.format(syst_err)
                else:
                    line += prec.format(info[0])
                    if 'data' not in s:
                        line += r" \pm " + prec.format(info[1])
                    if len(info) == 4:
                        line += "^{+"+prec.format(info[2])+"}_{"+prec.format(info[3])+"}"
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines
