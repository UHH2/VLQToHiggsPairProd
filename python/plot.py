#!/usr/bin/env python

import common_vlq
import settings

import os
import time
import varial.tools
import varial.generators as gen
from varial.sample import Sample
import varial.analysis as analysis
import normplots
import stackplots
import stackplots_sig


# varial.settings.use_parallel_chains = False

dir_norm_sig = 'NormedSignal'
dir_stack_sig = 'StackedSignal'
file_norm_sig = '*TpTp_M1000*.root'

dir_stack_all = 'StackedSigMerged'
file_stack_all = [f for f in os.listdir('.') if
    (f.endswith('.root') and 'M1000_' not in f
        # and 'HT' not in f
    )]

dir_stack_split = 'StackedSigSplit'
file_stack_split = [f for f in os.listdir('.') if
        (f.endswith('.root') and
            ('M1000_' not in f or any(w in f for w in [
                'thth',
                'thtz',
                'thbw',
                'bwbw',
                'tzbw',
                'tztz'
                ])
            )
            # and 'HT' not in f
        )]

dir_cutflow = 'Cutflows'





p1 = varial.tools.mk_rootfile_plotter(
    pattern= file_norm_sig,
    name=dir_norm_sig,
    plotter_factory=normplots.plotter_factory,
    combine_files=True,
)

p5 = varial.tools.mk_rootfile_plotter(
    pattern= file_norm_sig,
    name=dir_stack_sig,
    plotter_factory=stackplots_sig.plotter_factory,
    combine_files=True,
)

p2 = varial.tools.mk_rootfile_plotter(
    pattern= file_stack_all,
    name=dir_stack_all,
    plotter_factory=stackplots.plotter_factory,
    combine_files=True,
    # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
)

p3 = varial.tools.mk_rootfile_plotter(
    pattern= file_stack_split,
    name=dir_stack_split,
    plotter_factory=stackplots.plotter_factory,
    combine_files=True,
    # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
)

p4 = varial.tools.mk_rootfile_plotter(
    pattern=file_stack_split,
    name=dir_cutflow,
    plotter_factory=normplots.plotter_factory_cf,
    combine_files=True,
    filter_keyfunc=lambda w: 'Cutflow' in w.in_file_path
)

target_dir = 'Version0'

tc = varial.tools.ToolChain(
    target_dir,
    [
        p1,
        p5,
        p2,
        p3,
        p4
        ])

tc = varial.tools.ToolChain("", [tc])

if __name__ == '__main__':
    time.sleep(1)
    tc.run()
    os.chdir(target_dir)
    varial.tools.WebCreator().run()   
    # varial.tools.CopyTool('~/www/vlq_analysis/loose_selection/').run()
    os.chdir("..")

# working_dir='NormedSignal'

