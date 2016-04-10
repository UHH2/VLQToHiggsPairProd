#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector #, SGETreeProjector
from os.path import join
import varial.settings
import varial.tools
import glob
import os
import ast
import pprint

# varial.settings.max_num_processes = 24

iteration = [1]

core_histos = {
    'ST'                            : ('ST',                               45, 0, 4500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      14, -.5, 13.5),
    'n_ak8'                         : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'pt_ld_ak4_jet'                 : ('Pt leading Ak4 Jet',               60, 0., 1500.),
    'pt_ld_ak8_jet'                 : ('Pt leading Ak8 Jet',               60, 0., 1500.),
    'pt_subld_ak4_jet'              : ('Pt subleading Ak4 Jet',             60, 0., 1500.),
    'pt_subld_ak8_jet'              : ('Pt subleading Ak8 Jet',             60, 0., 1500.),
    'pt_third_ak4_jet'              : ('Pt third Ak4 Jet',             60, 0., 1500.),
    'pt_fourth_ak4_jet'              : ('Pt fourth Ak4 Jet',             60, 0., 1500.),
    'HT'                            : ('HT',                               45, 0, 4500),
    'met'                           : ('MET',                              50, 0., 1000.),
    'primary_lepton_pt'             : ('Primary Lepton p_T',               90, 0., 900.),
}


more_histos = {
    # 'gen_ht'                            : ('Gen HT',                               45, 0, 4500),
    # 'parton_ht'                            : ('Parton HT',                               45, 0, 4500),
    'primary_muon_pt'               : ('Primary Muon p_T',                 90, 0., 900.),
    'primary_electron_pt'           : ('Primary Electron p_T',             90, 0., 900.),
    # 'n_ak8_cleaned_dr'              : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'gendecay_accept'               : ('GenDecay Accept',                  2, -.5, 1.5),
    'n_additional_btags_medium'     : ('N(non-overlapping medium b-tags)', 8, -.5, 7.5),
    'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
    'n_higgs_tags_1b_med'           : ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    # 'n_higgs_tags_1b_med_cleaned_dr': ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    # 'n_higgs_tags_2b_med_cleaned_dr': ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    'n_jets_no_overlap'             : ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    'trigger_accept_mu45'           : ('Trigger Accepted Mu45',             2, -.5, 1.5),
    'trigger_accept_el45'           : ('Trigger Accepted El40',             2, -.5, 1.5),
    'trigger_accept_isoMu20'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'trigger_accept_isoEl27'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'is_muon'                       : ('Prim. Lep. is Muon',                2, -.5, 1.5),
    'pt_fifth_ak4_jet'              : ('Pt fifth Ak4 Jet',             60, 0., 1500.),
    'pt_sixth_ak4_jet'              : ('Pt sixth Ak4 Jet',             60, 0., 1500.),
    'pt_third_ak8_jet'              : ('Pt third Ak8 Jet',             60, 0., 1500.),
    # 'first_ak8jet_eta'                : ('Eta 1st Ak8 Jet',                  50, -3., 3.),
    # 'first_ak8jet_mass'               : ('Mass 1st Ak8 Jet',                 60, 0., 300.),
    # 'first_ak8jet_nsjbtags'           : ('N(med sj b-tags) 1st Ak8 Jet',     4, -.5, 3.5),
    # 'first_ak8jet_pt'                 : ('Pt 1st Ak8 Jet',                   60, 0., 1500.),
    # 'first_ak8jet_dRlep'                : ('dR(1st TopJet, primary lepton)',   50, 0., 5.),
    # 'first_ak8jet_dRak4'               : ('dR(1st TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    # 'first_ak8jet_dRak8'           : ('dR(1st TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    # 'second_ak8jet_eta'                : ('Eta 2nd Ak8 Jet',                  50, -3., 3.),
    # 'second_ak8jet_mass'               : ('Mass 2nd Ak8 Jet',                 60, 0., 300.),
    # 'second_ak8jet_nsjbtags'           : ('N(med sj b-tags) 2nd Ak8 Jet',     4, -.5, 3.5),
    # 'second_ak8jet_pt'                 : ('Pt 2nd Ak8 Jet',                   60, 0., 1500.),
    # 'second_ak8jet_dRlep'                : ('dR(2nd TopJet, primary lepton)',   50, 0., 5.),
    # 'second_ak8jet_dRak4'               : ('dR(2nd TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    # 'second_ak8jet_dRak8'           : ('dR(2nd TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    # 'higgs_tag_1b_eta'                : ('Eta Higgs-Tag(1b)',                  50, -3., 3.),
    # 'higgs_tag_1b_mass'               : ('Mass Higgs-Tag(1b)',                 60, 0., 300.),
    # 'higgs_tag_1b_nsjbtags'           : ('N(med sj b-tags) Higgs-Tag(1b)',     4, -.5, 3.5),
    # 'higgs_tag_1b_pt'                 : ('Pt Higgs-Tag(1b)',                   60, 0., 1500.),
    # 'higgs_tag_1b_dRlep'                : ('dR(Higgs-Tag(1b), primary lepton)',   50, 0., 5.),
    # 'higgs_tag_1b_dRak4'               : ('dR(Higgs-Tag(1b), nearest Ak4 Jet)',  50, 0., 5.),
    # 'higgs_tag_1b_dRak8'           : ('dR(Higgs-Tag(1b), nearest Ak8 Jet)',  50, 0., 5.),
    # 'higgs_tag_2b_eta'                : ('Eta Higgs-Tag(2b)',                  50, -3., 3.),
    # 'higgs_tag_2b_mass'               : ('Mass Higgs-Tag(2b)',                 60, 0., 300.),
    # 'higgs_tag_2b_nsjbtags'           : ('N(med sj b-tags) Higgs-Tag(2b)',     4, -.5, 3.5),
    # 'higgs_tag_2b_pt'                 : ('Pt Higgs-Tag(2b)',                   60, 0., 1500.),
    # 'higgs_tag_2b_dRlep'                : ('dR(Higgs-Tag(2b), primary lepton)',   50, 0., 5.),
    # 'higgs_tag_2b_dRak4'               : ('dR(Higgs-Tag(2b), nearest Ak4 Jet)',  50, 0., 5.),
    # 'higgs_tag_2b_dRak8'           : ('dR(Higgs-Tag(2b), nearest Ak8 Jet)',  50, 0., 5.),
    # 'use_sr_sf'                     : ('Use SR SF',                         2, -.5, 1.5),
}
more_histos.update(core_histos)

params = {
    'histos': more_histos,
    'treename': 'AnalysisTree',
}

signals = [
    'TpTp_M-0700',
    'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
    'TpTp_M-1700',
    'TpTp_M-1800',
]

final_states = [
    '_thth',
    # '_thtz',
    # '_thbw',
    # '_noH_tztz',
    # '_noH_tzbw',
    # '_noH_bwbw',
]

background_samples = [
    'TTbar',
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
]

signal_samples = reduce(lambda x, y: x+y, (list(g + f for f in final_states) for g in signals))

samples = background_samples + signal_samples + ['Run2015CD']
samples_no_data = background_samples + signal_samples

base_weight = 'weight'

# # values below from FinalSelection-v14/RunWJetsSideband/fit_results_ht_sideband_w_toppt_reweight.txt
# # p0_from1000 = 1.252481
# # p1_from1000 = -0.000216602

# # p0_from0 = 1.353281
# # p1_from0 = -0.000251745

# # values below from FinalSelection-v14/RunWJetsSideband/fit_results_ht_sideband_w_toppt_reweight.txt

# p0_from0_no_top_pt_reweight = 1.165688
# p1_from0_no_top_pt_reweight = -0.000236061

# ht_reweight = '*({0}+{1}*HT)'.format(p0_from0_no_top_pt_reweight, p1_from0_no_top_pt_reweight)
# ttbar_reweight = '*(weight_ttbar/0.9910819)'

sample_weights_def = {
    'TTbar' : base_weight,
    'SingleTop' : base_weight,
    'QCD' : base_weight,
    'DYJets' : base_weight,
    'WJets' : base_weight,
    'Run2015CD' : '1',
}
sample_weights_def.update(dict((f, 'weight') for f in signal_samples))


# import tptp_selections_treeproject as sel


sys_params = {
    'histos': core_histos,
    'treename': 'AnalysisTree',
}


def mk_tp(input_pat, final_regions, weights=None, samples=samples, name='TreeProjector'):
    sample_weights = weights or sample_weights_def
    sec_sel_weight = list((g, f, weights) for g, f in final_regions)
    all_files = glob.glob(join(input_pat, 'Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.*.root'))
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    return TreeProjector(
        filenames, params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name=name,
    )

def add_jec_uncerts(base_path, final_regions, sample_weights):
    # def tmp():
    jercs = list(
        (
            name.replace('_down', '__minus').replace('_up', '__plus'), 
            join(base_path, 'Files_and_Plots_' + name + '/SFrame/workdir/uhh2*.root')
        ) 
        for name in ('jec_down', 'jec_up', 'jer_down', 'jer_up')
    )
    nominal_sec_sel_weight = list((g, f, sample_weights) for g, f in final_regions)
    return list(
        TreeProjector(
            dict(
                (sample, list(f for f in glob.glob(pat) if sample in f))
                for sample in samples_no_data
            ), 
            sys_params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, pat in jercs
    )
    # return tmp

def add_generic_uncerts(base_path, final_regions, sample_weights):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    sys_sec_sel_weight = list(
        (name, list((g, f, dict((a, c+w) for a, c in sample_weights.iteritems()))
            for g, f in final_regions) 
        )
        for name, w in (
            ('btag_bc__minus', '*weight_btag_bc_down/weight_btag'),
            ('btag_bc__plus', '*weight_btag_bc_up/weight_btag'),
            ('btag_udsg__minus', '*weight_btag_udsg_down/weight_btag'),
            ('btag_udsg__plus', '*weight_btag_udsg_up/weight_btag'),
            ('sfmu_id__minus', '*weight_sfmu_id_down/weight_sfmu_id'),
            ('sfmu_id__plus', '*weight_sfmu_id_up/weight_sfmu_id'),
            ('sfmu_trg__minus', '*weight_sfmu_trg_down/weight_sfmu_trg'),
            ('sfmu_trg__plus', '*weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pu__minus', '*weight_pu_down/weight_pu'),
            ('pu__plus', '*weight_pu_up/weight_pu'),
            ('rate__minus', '*0.95'), # for 2D-cut and el/add. mu trg uncertainty
            ('rate__plus', '*1.05'), # for 2D-cut and el/add. mu trg uncertainty
            # ('ak4_jetpt__minus', '*weight_ak4_jetpt_down/weight_ak4_jetpt'),
            # ('ak4_jetpt__plus', '*weight_ak4_jetpt_up/weight_ak4_jetpt'),
        )
    )
    return list(
        TreeProjector(
            filenames,
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight
    )
    # return tmp


def add_pdf_uncerts(base_path, final_regions, sample_weights):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    with open('weight_dict_pdf') as f:
        weight_dict_pdf = ast.literal_eval(f.read())
    weight_dict_pdf.update(dict((smpl, ['1']*100) for smpl in background_samples))
    for g in final_states:
        weight_dict_pdf.update(dict((s+g, weight_dict_pdf[s]) for s in signals))
    # sys_params_pdf = {
    #     'histos': core_histos,
    #     'treename': 'AnalysisTree',
    # }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, list((g, f,
            dict(
                    (smpl, sample_weights[smpl]+'*weight_pdf_%i/%s'%(i, weight_dict[i]))
                    for smpl, weight_dict in weight_dict_pdf.iteritems() if smpl in samples_no_data
                )
            ) for g, f in final_regions)
        )
        for i in xrange(100)
    )
    sys_tps_pdf = list(
        TreeProjector(
            filenames, 
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight_pdf
    )
    sys_tps_pdf += [GenUncertHistoSquash(squash_func=varial.op.squash_sys_stddev)]
    return [
        varial.tools.ToolChain('SysTreeProjectorsPDF', sys_tps_pdf),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', name='PDF__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', name='PDF__minus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', norm=True, name='NormPDF__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', norm=True, name='NormPDF__minus'),
    ]
    # return tmp


def add_scale_var_uncerts(base_path, final_regions, sample_weights):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    with open('weight_dict_scale') as f:
        weight_dict_scale = ast.literal_eval(f.read())
    weight_dict_scale.update(dict((smpl, ['1']*9) for smpl in background_samples))
    for g in final_states:
        weight_dict_scale.update(dict((s+g, weight_dict_scale[s]) for s in signals))
    sys_sec_sel_weight_scalevar = list(
        ('scalevar_weight_%i'%i, list((g, f,
            dict(
                    (smpl, sample_weights[smpl]+'*weight_muRF_%i/%s'%(i, weight_dict[i]))
                    for smpl, weight_dict in weight_dict_scale.iteritems() if smpl in samples_no_data
                )
            ) for g, f in final_regions)
        )
        for i in [1, 2, 3, 4, 6, 8] # physical indices for scale variations without nominal value!
        # for i in [1, 2] # physical indices for scale variations without nominal value!
    )
    sys_tps_scalevar = list(
        TreeProjector(
            filenames, 
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight_scalevar
    )
    sys_tps_scalevar += [GenUncertHistoSquash(squash_func=varial.op.squash_sys_env)]
    return [
        varial.tools.ToolChain('SysTreeProjectorsScaleVar', sys_tps_scalevar),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', name='ScaleVar__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', name='ScaleVar__minus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', norm=True, name='NormScaleVar__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', norm=True, name='NormScaleVar__minus'),
    ]
    # return tmp


def add_weight_uncerts(base_path, final_regions, sample_weights, weight_name, weight_dict):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    sample_weights_reweight_down = dict(sample_weights)
    sample_weights_reweight_up = dict(sample_weights)
    sample_weights_reweight_down.update(dict((proc, sample_weights[proc]+'*'+weight) for proc, weight in weight_dict.iteritems()))
    sample_weights_reweight_up.update(dict((proc, sample_weights[proc]+'/'+weight) for proc, weight in weight_dict.iteritems()))
    # print 'SAMPLE_WEIGHTS'
    # pprint.pprint(sample_weights)
    # print 'SAMPLE_WEIGHTS_REWEIGHT_DOWN'
    # pprint.pprint(sample_weights_reweight_down)
    # print 'SAMPLE_WEIGHTS_REWEIGHT_UP'
    # pprint.pprint(sample_weights_reweight_up)
    sys_sec_sel_weight_reweight_weight = (
        (weight_name+'__minus', list((g, f, sample_weights_reweight_down) for g, f in final_regions)),
        (weight_name+'__plus', list((g, f, sample_weights_reweight_up) for g, f in final_regions))
    )
    return list(
        TreeProjector(
            filenames,
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight_reweight_weight
    )
    # return tmp

def mk_sys_tps(mk_sys_func, name='SysTreeProjectors'):
    # sample_weights = weights or sample_weights_def
    # some defs
    # base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/'\
    #     'CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'\
    #     'TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'

    # first put together jerc uncert with nominal weights
    if mk_sys_func:
        sys_tps = mk_sys_func()
    else:
        sys_tps = []

    # next put together nominal samples with with weight uncerts.
    

    # PDF uncertainties
    

    # Scale Variation uncertainties
    

    for tp in sys_tps:
        iteration[0] += 1
        tp.iteration = 10 * iteration[0]  # batch tp's should not interfere

    return varial.tools.ToolChain(
        name, sys_tps
    )


class GenUncertHistoSquash(varial.tools.Tool):
    io = varial.pklio

    def __init__(self, squash_func=varial.op.squash_sys_stddev, sample='', **kws):
        super(GenUncertHistoSquash, self).__init__(**kws)
        self.squash_func = squash_func
        self.sample = sample
        self.rel_path = '*.root'
        if self.sample:
            self.name = 'GenUncertHistoSquash_'+sample
            self.relpath = self.sample+'.root'

    def run(self):
        pdf_paths = glob.glob(self.cwd + '../*')
        pdf_paths.remove(self.cwd + '../'+self.name)
        uncert_histos = (
            w
            for p in pdf_paths
            for w in varial.diskio.bulk_load_histograms(
                        varial.gen.dir_content(p+'/%s'%self.rel_path))
                        # varial.gen.dir_content(p+'/%s.root'%self.sample))
        )
        uncert_histos = sorted(uncert_histos, key=lambda w: w.sample)
        uncert_histos = sorted(uncert_histos, key=lambda w: w.in_file_path.split('/')[0])
        uncert_histos = sorted(uncert_histos, key=lambda w: w.in_file_path.split('/')[1])
        # uncert_histos = list(uncert_histos)
        # for w in uncert_histos: print w.sample, w.file_path, w.in_file_path
        uncert_histos = varial.gen.group(uncert_histos, lambda w: w.sample)
        # uncert_histos = list(uncert_histos)
        # for p in uncert_histos: print list((g.file_path, g.in_file_path) for g in p)
        uncert_histos = (self.squash_func(h) for h in uncert_histos)
        self.result = list(uncert_histos)
        os.system('touch %s/webcreate_denial' % self.cwd)


class GenUncertUpDown(varial.tools.Tool):
    io = varial.pklio

    def __init__(self, input_path, norm=False, **kws):
        super(GenUncertUpDown, self).__init__(**kws)
        self.input_path = input_path
        self.norm = norm

    def run(self):
        assert '__plus' in self.name or '__minus' in self.name
        factor = 1. if '__plus' in self.name else -1.
        self.message('INFO adding error with factor: %i' % factor)

        def set_values(w):
            h = w.histo
            if w.histo_sys_err:
                h_sys = w.histo_sys_err
            else:
                h_sys = w.histo
            for i in xrange(h_sys.GetNbinsX()+2):
                h.SetBinContent(i, h_sys.GetBinContent(i) 
                                   + factor*h_sys.GetBinError(i))
            w.histo_sys_err = None
            return w

        def norm_thing(wrps):
            sigs = varial.gen.dir_content('../../TreeProjector/*.root')
            # sigs = (s for s in sigs if '/TpTp_' in s.file_path)
            sigs = (s for s in sigs if s.name in core_histos.keys())
            # sigs = (s for s in sigs if 'SignalRegion' in s.in_file_path)
            sigs = varial.gen.load(sigs)
            sigs = varial.gen.gen_add_wrp_info(sigs, 
                category=lambda w: w.in_file_path.split('/')[0])
            sigs = dict((s.sample+'_'+s.name+'_'+s.category, s.histo) for s in sigs)
            for w in wrps:
                w.histo.Scale(sigs[w.sample+'_'+w.name+'_'+w.category].Integral() / w.histo.Integral())
                yield w

        from itertools import groupby

        def store(grps):
            for g in grps:
                sample = g.wrps[0].sample
                wrps = sorted(g.wrps, key=lambda a: a.category)
                wrps = dict((k, list(w)) for k, w in groupby(wrps, key=lambda a: a.category))
                for k, ws in wrps.iteritems():
                    fsw = varial.analysis.fileservice(k)
                    for w in ws: fsw.append(w.histo)
                varial.diskio.write_fileservice(sample)
                yield g


        input_list = glob.glob(os.path.join(self.cwd, self.input_path)) # '../SysTreeProjectorsPDF/GenUncertHistoSquash*'
        # print input_list
        histos = list(self.lookup_result(k) for k in input_list)
        histos = list(h for g in histos for h in g)
        assert histos

        histos = (varial.op.copy(w) for w in histos)
        histos = varial.gen.gen_add_wrp_info(histos, 
            category=lambda w: w.in_file_path.split('/')[0],
            variable=lambda w: w.in_file_path.split('/')[1])
        histos = (set_values(w) for w in histos)
        if self.norm:
            histos = norm_thing(histos)
        histos = sorted(histos, key=lambda w: w.sample)
        histos = varial.gen.group(histos, lambda w: w.sample)
        histos = store(histos)
        histos = list(histos)

        alia = varial.diskio.generate_aliases(self.cwd + '*.root')
        alia = varial.gen.gen_add_wrp_info(alia, 
            sample=lambda a: os.path.basename(os.path.splitext(a.file_path)[0]))
        self.result = list(alia)
        os.system('touch %s/aliases.in.result' % self.cwd)
        os.system('touch %s/webcreate_denial' % self.cwd)

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Input file pattern needed!'
        exit(-1)
    input_pat = sys.argv[1]
    varial.tools.Runner(mk_tp(input_pat))

