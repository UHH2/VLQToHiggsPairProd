#!/usr/bin/env python

import common_vlq
import settings
import sys

import os
import time
import varial.tools
import varial.generators as gen
from varial.sample import Sample
import varial.analysis as analysis
import normplots
import stackplots
import stackplots_sig
import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# if len(sys.argv) > 1:
#     target_dir = sys.argv[1]
#     if not target_dir.endswith('/'):
#         target_dir += '/'
# else:
#     target_dir = ''

src_dir_rel = '../SFrame'

# varial.settings.use_parallel_chains = False

normfactor = 1.

def only_tptp(filename):
    return not ('BpJ' in filename or 'TpJ' in filename)

# legend_preselection = {
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',
#     src_dir+'/uhh2.AnalysisModuleRunner.MC.MC_TTJets_20x25.root' : 'TTJets',

# }

def file_stack_all():
    src_dir = varial.analysis.cwd+src_dir_rel
    file_stack_all_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
        (f.endswith('.root')
        )]
    return file_stack_all_list

final_dir = 'Plots'

def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=file_stack_all(),
            name='Cutflows',
            plotter_factory=normplots.plotter_factory_cf,
            combine_files=True,
            filter_keyfunc=lambda w: 'Cutflow' in w.in_file_path
            ),
        varial.tools.mk_rootfile_plotter(
            pattern= file_stack_all(),
            name='StackedAll',
            plotter_factory=lambda **w: stackplots.plotter_factory(normfactor, **w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        ]

if __name__ == '__main__':
    time.sleep(1)
    all_tools = mk_tools()
    tc = varial.tools.ToolChain(
        final_dir, all_tools)
    varial.tools.Runner(tc)
    # varial.tools.WebCreator(no_tool_check=True).run()   
    for itool in all_tools:
        dir_name = os.path.join('./'+final_dir, itool.name)
        print dir_name
        varial.tools.WebCreator(working_dir=dir_name).run()
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()

# working_dir='NormedSignal'

