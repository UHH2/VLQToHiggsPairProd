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

order_cats = ['Preselection', 'Sideband', 'H1B category', 'H2B category']
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





class EffNumTable(varial.tools.Tool):
    def __init__(self, input_blocks, get_region, calc_eff=False, name=None):
        super(EffNumTable, self).__init__(name)
        self.input_blocks = input_blocks
        self.get_region = get_region
        self.calc_eff = calc_eff

    def mk_filter(self, smpl):
        def tmp(path):
            return smpl in path and path.endswith('ST')
        return tmp

    def get_precision(self, num):
        if num >= 1.0:
            return "%17.1f"
        elif num > 0:
            ex_dim = abs(floor(log10(num)))
            add_prec = 0
            if num*10**ex_dim < 2.:
                add_prec = 1
            prec = int(ex_dim+add_prec)
            prec = "%17."+str(prec)+"f"
            return prec
        else:
            return "%17d"

    def prepare(self, samples, path):
        def get_path(path):
            if not os.path.exists(path):
                return os.path.join(self.cwd, path)
            else:
                return path
        

        if isinstance(samples, dict):
            smpls = samples
        elif isinstance(samples, collections.Iterable) and not isinstance(samples, str):
            smpls = dict((s, self.mk_filter(s)) for s in samples)
        else:
            self.message('ERROR! Need to provide list of samples or dict!')


        smpl_tup = list((s, fs) for s, fs in smpls.items())
        smpl_tup = sorted(smpl_tup, key=sort_cats(order_smpls))

        if isinstance(path, collections.Iterable) and not isinstance(path, str):
            res = (os.path.join(get_path(p), '_varial_infodata.pkl')
                for p in path
            )
            res = list(res)
            res = dict((fname, dict((k, i) for k, i in cPickle.load(open(fname)).items())) for fname in res)
        elif isinstance(path, str):
            res = cPickle.load(open(os.path.join(get_path(path), '_varial_infodata.pkl')))

        return smpl_tup, res

    def get_info(self, region, sample, filt_smpls, filt_func, res, key_word):
        rgns = list(itertools.ifilter(filt_func, filt_smpls))
        if len(rgns) > 1:
            self.message('WARNING! More than one region found for region %s and sample %s!' % (region, sample))
            return
        if len(rgns) == 0:
            self.message('WARNING! Nothing found for region %s and sample %s!' % (region, sample))
            return
        info = res[rgns[0]]
        if not key_word or not key_word in info.keys():
            key = list(itertools.ifilter(lambda w: sample in w, info))
            if len(key) == 1:
                key = key[0]
            elif len(key) > 1:
                self.message('WARNING! More than one key word found for sample '+sample)
            else:
                self.message('WARNING! No key word found for sample '+sample)
        else:
            key = key_word
        return info[key]

    def create_count_block(self, samples, path, key_word='Integral___bkg_sum'):

        smpl_tup, res = self.prepare(samples, path)

        lines = []
        for s, fs in smpl_tup:
            filt_smpls = list(itertools.ifilter(fs, res))
            line = s + " "
            for r, fr in self.get_region:
                line += "&$ "
                info = self.get_info(r, s, filt_smpls, fr, res, key_word)
                if not info:
                    continue
                if 'data' in key_word:
                    prec = "%17d"
                else:
                    prec = self.get_precision(info[1])
                line += prec % info[0] + r" \pm " + prec % info[1]
                if len(info) == 4:
                    syst_string = "^{+"+prec+"}_{"+prec+"}"
                    line += syst_string % (info[2], info[3])
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines


    def create_eff_block(self, samples, path, baseline, key_word='Integral___bkg_sum'):

        smpl_tup, res = self.prepare(samples, path)

        lines = []
        for s, fs in smpl_tup:
            filt_smpls = list(itertools.ifilter(fs, res))
            line = s + " "
            if isinstance(baseline, dict): 
                baseline_count = baseline[s]
            else:
                baseline_count = baseline
            for r, fr in self.get_region:
                line += "&$ "
                info = self.get_info(r, s, filt_smpls, fr, res, key_word)
                if not info:
                    continue
                # prec = eff_prec.get(s, "%.1f")
                prec_string = " "+self.get_precision(info[1]/baseline_count*100.)+r" \%% \pm "+self.get_precision(info[1]/baseline_count*100.)+r" \%%"
                line += prec_string % (info[0]/baseline_count*100., info[1]/baseline_count*100.)
                if len(info) == 4:
                    syst_string = "^{+"+self.get_precision(info[1]/baseline_count*100.)+r" \%%}_{"+self.get_precision(info[1]/baseline_count*100.)+r" \%%}"
                    line += syst_string % (info[2]/baseline_count*100., info[3]/baseline_count*100.)
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines

        

    def run(self):

        if not isinstance(self.get_region, dict):
            self.get_region = dict((s, self.mk_filter(s)) for s in self.get_region)

        region_tup = list((r, fr) for r, fr in self.get_region.items())
        region_tup = sorted(region_tup, key=sort_cats(order_cats))
        self.get_region = region_tup
        lines = []
        lines.append(r"\begin{tabular}{|l "
            + len(self.get_region)*"| r "
            + r"|}\hline")
        lines.append("process / category & " + r" & ".join(r[0] for r in self.get_region)
            + r"\\ \hline")
        if not self.calc_eff:
            for smpls, path, key_word in self.input_blocks:
                lines += self.create_count_block(smpls, path, key_word)
                lines.append(r"\hline")
        else:
            for smpls, path, baseline, key_word in self.input_blocks:
                lines += self.create_eff_block(smpls, path, baseline, key_word)
                lines.append(r"\hline")

        
        lines.append(r"\end{tabular}")


        lines = '\n'.join(lines)
        with open(self.cwd+'count_table_content.tex', 'w') as f:
            f.write(lines)





class NumTableNew(varial.tools.Tool):
    def __init__(self, input_blocks, get_region, name=None):
        super(NumTableNew, self).__init__(name)
        self.input_blocks = input_blocks
        self.regions = get_region

    def get_precision(self, num):
        if num >= 1.0:
            return "%17.1f"
        elif num > 0:
            ex_dim = abs(floor(log10(num)))
            add_prec = 0
            if num*10**ex_dim < 2.:
                add_prec = 1
            prec = int(ex_dim+add_prec)
            prec = "%17."+str(prec)+"f"
            return prec
        else:
            return "%17d"

    def create_block(self, sample_dict):
        pass
        

    def run(self):
        
        self.regions = list((r, f(self.cwd)) for r, f in self.regions)
        self.regions = sorted(self.regions, key=sort_cats(order_cats))

        lines = []
        lines.append(r"\begin{tabular}{|l "
            + len(self.regions)*"| r "
            + r"|}\hline")
        lines.append("process / category & " + r" & ".join(r for r, _ in self.regions)
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
    def __init__(self, input_blocks, get_region, norm_fct, name=None):
        super(EffTable, self).__init__(input_blocks, get_region, name)
        self.norm_fct = norm_fct

    def create_block(self, sample_dict):

        lines = []
        for s, s_func in sample_dict:
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
                    prec = "%17d"
                else:
                    prec = self.get_precision(info[1]/baseline_count)
                line += prec % (info[0]/baseline_count) + r" \%% \pm " + prec % (info[1]/baseline_count) + r" \%%"
                if len(info) == 4:
                    syst_string = "^{+"+prec+r" \%%}_{"+prec+r" \%%}"
                    line += syst_string % ((info[2]/baseline_count), (info[3]/baseline_count))
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines

class CountTable(NumTableNew):
    def __init__(self, input_blocks, get_region, name=None):
        super(CountTable, self).__init__(input_blocks, get_region, name)

    def create_block(self, sample_dict):

        lines = []
        for s, s_func in sample_dict:
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
                    prec = "%17d"
                else:
                    prec = self.get_precision(info[1])
                line += prec % info[0] + r" \pm " + prec % info[1]
                if len(info) == 4:
                    syst_string = "^{+"+prec+"}_{"+prec+"}"
                    line += syst_string % (info[2], info[3])
                line += " $"
            line += r" \\"
            lines.append(line)
        return lines