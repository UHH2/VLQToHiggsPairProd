#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector #, SGETreeProjector
from os.path import join
import varial.tools
import glob
import os

# varial.settings.max_num_processes = 24

iteration = [1]

core_histos = {
    'ST'                            : ('ST',                               45, 0, 4500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      14, -.5, 13.5),
    'n_ak8_cleaned'                         : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'pt_ld_ak4_jet'                 : ('Pt leading Ak4 Jet',               60, 0., 1500.),
    'pt_ld_ak8_jet'                 : ('Pt leading Ak8 Jet',               60, 0., 1500.),
    # 'primary_lepton_pt'             : ('Primary Lepton p_T',               90, 0., 900.),
}

more_histos = {
    'gendecay_accept'               : ('GenDecay Accept',                  2, -.5, 1.5),
    # 'ST_cleaned'                    : ('ST cleaned',                       45, 0, 4500),
    'n_additional_btags_medium'     : ('N(non-overlapping medium b-tags)', 8, -.5, 7.5),
    # 'n_ak4_pt_cleaned'              : ('N(Ak4 Jets, cleaned)',             14, -.5, 13.5),
    # 'n_ak8_pt_cleaned'              : ('N(Ak8 Jets, cleaned)',             8, -.5, 7.5),
    'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
    'n_higgs_tags_1b_med'           : ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    'n_jets_no_overlap'             : ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    'pt_subld_ak4_jet'              : ('Pt subleading Ak4 Jet',             60, 0., 1500.),
    # 'pt_ld_ak4_jet_cleaned'         : ('Pt leading Ak4 Jet, cleaned',      60, 0., 1500.),
    # 'pt_ld_ak8_jet_cleaned'         : ('Pt leading Ak8 Jet, cleaned',      60, 0., 1500.),
    'trigger_accept_mu45'           : ('Trigger Accepted Mu45',             2, -.5, 1.5),
    'trigger_accept_el45'           : ('Trigger Accepted El40',             2, -.5, 1.5),
    'trigger_accept_isoMu20'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'trigger_accept_isoEl27'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'is_muon'                       : ('Prim. Lep. is Muon',                2, -.5, 1.5),
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

samples = background_samples + signal_samples + ['Run2015D']
samples_no_data = background_samples + signal_samples

sample_weights = {
    'TTbar' : 'weight*weight_ak4_jetpt',
    'SingleTop' : 'weight*weight_ak4_jetpt',
    'QCD' : 'weight*weight_ak4_jetpt',
    'DYJets' : 'weight*weight_ak4_jetpt',
    'WJets' : 'weight*weight_ak4_jetpt',
    'Run2015D' : 'weight',
}
sample_weights.update(dict((f, 'weight') for f in signal_samples))

base_weight = 'weight'

sample_weights_pdf = [
    'TTbar',
    # 'SingleTop',
    'DYJets',
    'WJets',
] + signal_samples

import tptp_selections_treeproject as sel

final_regions = {
    'BaseLineSelectionEl45' : sel.el_channel,
    'BaseLineSelectionMu45' : sel.mu_channel,
    'SignalRegion2b_El45' : sel.sr2b_channel + sel.el_channel,
    'SignalRegion1b_El45' : sel.sr1b_channel + sel.el_channel,
    'SidebandRegion_El45' : sel.sb_channel + sel.el_channel,
    'SignalRegion2b_Mu45' : sel.sr2b_channel + sel.mu_channel,
    'SignalRegion1b_Mu45' : sel.sr1b_channel + sel.mu_channel,
    'SidebandRegion_Mu45' : sel.sb_channel + sel.mu_channel,
}


sec_sel_weight = list((g, f, sample_weights) for g, f in final_regions.iteritems())

# [
#     ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
#     ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
#     # ('BaseLineSelection', sel.baseline_selection, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
#     ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
#     ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
#     ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
#     ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
#     ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
#     ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
# ]


def mk_tp(input_pat):
    all_files = glob.glob(join(input_pat, 'Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.*.root'))
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    return TreeProjector(
        filenames, params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name='TreeProjector',
    )


def mk_sys_tps(base_path):
    # some defs
    # base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/'\
    #     'CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'\
    #     'TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'
    sys_params = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
    }

    # first put together jerc uncert with nominal weights
    jercs = list(
        (
            name.replace('_down', '__minus').replace('_up', '__plus'), 
            join(base_path, 'Files_and_Plots_' + name + '/SFrame/workdir/uhh2*.root')
        ) 
        for name in ('jec_down', 'jec_up', 'jer_down', 'jer_up')
    )
    nominal_sec_sel_weight = list((g, f, sample_weights) for g, f in final_regions.iteritems())
    # [
    #     ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
    #     ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
    #     ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights),
    #     ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights),
    #     ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights),
    #     ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights),
    #     ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights),
    #     ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights),
    # ]
    sys_tps = []
    # sys_tps = list(
    #     TreeProjector(
    #         dict(
    #             (sample, list(f for f in glob.glob(pat) if sample in f))
    #             for sample in samples_no_data
    #         ), 
    #         sys_params, 
    #         nominal_sec_sel_weight,
    #         add_aliases_to_analysis=False,
    #         name=name,
    #     )
    #     for name, pat in jercs
    # )

    # next put together nominal samples with with weight uncerts.
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    sys_sec_sel_weight = list(
        (name, list((g, f, dict((a, f+w) for a, f in sample_weights.iteritems()))
            for g, f in final_regions.iteritems()) 
        #     [
        #     ('BaseLineSelectionEl45', sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())), # *weight_ak4_jetpt
        #     ('BaseLineSelectionMu45', sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())), # *weight_ak4_jetpt
        #     # ('BaseLineSelection', sel.baseline_selection, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        #     ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        # ]
        )
        # (name, [
        #     ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
        #     ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
        #     ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights),
        #     ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights),
        #     ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights),
        #     ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights),
        #     ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights),
        #     ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights),
        # ])
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
            ('ak4_jetpt__minus', '*weight_ak4_jetpt_down/weight_ak4_jetpt'),
            ('ak4_jetpt__plus', '*weight_ak4_jetpt_up/weight_ak4_jetpt'),
        )
    )
    # sys_tps += list(
    #     TreeProjector(
    #         filenames,
    #         sys_params, 
    #         ssw,
    #         add_aliases_to_analysis=False,
    #         name=name,
    #     )
    #     for name, ssw in sys_sec_sel_weight
    # )

    # PDF uncertainties
    # with open('weight_dict_TpB') as f:
    #     weight_dict = ast.literal_eval(f.read())
    # with open('weight_dict_TpT') as f:
    #     weight_dict.update(ast.literal_eval(f.read()))
    sys_params_pdf = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
    }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, list((g, f,
            dict(
                    (smpl, base_weight+'*weight_pdf_%i'%i)
                    for smpl in sample_weights_pdf
                )
            ) for g, f in final_regions.iteritems())
        #     list(
        #     (
        #         'SignalRegion',
        #         sr_sel,
        #         dict(
        #             (smpl, base_weight+'*weight_pdf_%i/%s'%i)
        #             for smpl, weight_list in weight_dict.iteritems()
        #         )
        #     ),
        # ) for reg in 
        )
        for i in xrange(100)
    )
    filenames_pdf = dict(
        (s, fs)
        for s, fs in filenames.iteritems()
        if s in sample_weights_pdf
    )
    sys_tps_pdf = list(
        TreeProjector(
            filenames_pdf, 
            sys_params_pdf, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight_pdf
    )
    sys_tps_pdf.append(PDFHistoSquash())
    sys_tps += [
        varial.tools.ToolChain('SysTreeProjectorsPDF', sys_tps_pdf),
        PDFUpDown(name='PDF__plus'),
        PDFUpDown(name='PDF__minus'),
    ]

    for tp in sys_tps:
        iteration[0] += 1
        tp.iteration = 10 * iteration[0]  # batch tp's should not interfere

    # make it complete with a tooloolchain!
    return varial.tools.ToolChain(
        'SysTreeProjectors', sys_tps
    )



    # make it complete with a tooloolchain!
    return varial.tools.ToolChain(
        'SysTreeProjectors', sys_tps
    )

class PDFHistoSquash(varial.tools.Tool):
    io = varial.pklio

    def run(self):
        pdf_paths = glob.glob(self.cwd + '../*')
        pdf_paths.remove(self.cwd + '../PDFHistoSquash')
        pdf_histos = (
            w
            for p in pdf_paths
            for w in varial.diskio.bulk_load_histograms(
                        varial.gen.dir_content(p+'/*.root'))
        )
        pdf_histos = sorted(pdf_histos, key=lambda w: w.sample)
        pdf_histos = sorted(pdf_histos, key=lambda w: w.in_file_path.split('/')[0])
        pdf_histos = sorted(pdf_histos, key=lambda w: w.in_file_path.split('/')[1])
        # pdf_histos = list(pdf_histos)
        # for w in pdf_histos: print w.sample, w.file_path, w.in_file_path
        pdf_histos = varial.gen.group(pdf_histos, lambda w: w.sample)
        # pdf_histos = list(pdf_histos)
        # for p in pdf_histos: print list((g.file_path, g.in_file_path) for g in p)
        pdf_histos = (varial.op.squash_sys_stddev(h) for h in pdf_histos)
        self.result = list(pdf_histos)
        os.system('touch %s/webcreate_denial' % self.cwd)


class PDFUpDown(varial.tools.Tool):
    io = varial.pklio

    def run(self):
        assert '__plus' in self.name or '__minus' in self.name
        factor = 1. if '__plus' in self.name else -1.
        self.message('INFO adding error with factor: %i' % factor)

        def set_values(w):
            h = w.histo
            h_sys = w.histo_sys_err
            for i in xrange(h_sys.GetNbinsX()+2):
                h.SetBinContent(i, h_sys.GetBinContent(i) 
                                   + factor*h_sys.GetBinError(i))
            w.histo_sys_err = None
            return w

        def norm_thing(wrps):
            sigs = varial.gen.dir_content('../../TreeProjector/*.root')
            sigs = (s for s in sigs if '/Signal_' in s.file_path)
            sigs = (s for s in sigs if s.name == 'vlq_mass')
            sigs = (s for s in sigs if 'SignalRegion' in s.in_file_path)
            sigs = varial.gen.load(sigs)
            sigs = dict((s.sample, s.histo) for s in sigs)
            for w in wrps:
                w.histo.Scale(sigs[w.sample].Integral() / w.histo.Integral())
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





        histos = self.lookup_result('../SysTreeProjectorsPDF/PDFHistoSquash')
        assert histos

        histos = (varial.op.copy(w) for w in histos)
        histos = (set_values(w) for w in histos)
        # histos = norm_thing(histos)
        histos = varial.gen.gen_add_wrp_info(histos, 
            category=lambda w: w.in_file_path.split('/')[0],
            variable=lambda w: w.in_file_path.split('/')[1])
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

