#!/usr/bin/env python

import os
import time

import common_vlq
import common_sensitivity
import varial.tools
import varial.generators as gen
import varial.analysis as analysis
import varial.wrappers as wrappers

from varial.sample import Sample
from varial.extensions.limits import *

import theta_auto
import model_vlqpair

varial.settings.use_parallel_chains = False

theta_auto.config.theta_dir = "/nfs/dust/cms/user/nowatsd/theta"

dir_limit = 'Limits_v0_test3_triangleplots'

file_stack_all = [f for f in os.listdir('.') if
    (f.endswith('.root') and 'M1000_' not in f
        # and 'HT' not in f
    )]

file_stack_split = [f for f in os.listdir('.') if
    (f.endswith('.root') and not f.endswith('_M1000.root')
        # and 'HT' not in f
    )]

# brs0 = {
#     'bw' : 0.5,
#     'th' : 0.25,
#     'tz' : 0.25
# }

# brs1 = {
#     'bw' : 0.333,
#     'th' : 0.333,
#     'tz' : 0.333
# }

br_list = []

for th_br in [i/10. for i in range(0, 12, 2)]:
    for tz_br in [ii/10. for ii in range(0, int(12-th_br*10), 2)]:
        bw_br = 1-th_br-tz_br
        # print bw_br, th_br, tz_br
        br_list.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

tool_list = []

def loader_hook_func(brs):
    def temp(w):
        return common_sensitivity.loader_hook_scale(w, brs)
    return temp

for ind, brs_ in enumerate(br_list):
    print 'ITERATION '+str(ind)
    print brs_
    tool_list.append(
        varial.tools.HistoLoader(
            name='HistoLoaderSplit'+str(ind),
            pattern=file_stack_split,
            filter_keyfunc=lambda w: w.in_file_path == 'EventHistsPost/EventHists/ST',
            hook_loaded_histos=loader_hook_func(brs_)
        ))
    tool_list.append(
        TpTpThetaLimits(
            input_path= '../HistoLoaderSplit'+str(ind),
            name= 'ThetaLimitsSplit'+str(ind),
            # asymptotic= False,
            brs=brs_,
            model_func= lambda w: model_vlqpair.get_model(w, ['TpTp_M1000'])
        ))

tool_list.append(TriangleLimitPlots())

tc = varial.tools.ToolChain(
    dir_limit, tool_list
)

# tc = varial.tools.ToolChain("", [tc])

if __name__ == '__main__':
    time.sleep(1)
    varial.tools.Runner(tc)
    os.chdir(dir_limit)
    # varial.tools.WebCreator().run()
    os.chdir('..') 

