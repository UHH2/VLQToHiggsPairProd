#!/usr/bin/env python


# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as common
import loose_sframe
import tight_sframe
# import sensitivity
# import tex_content

import varial.tools
import varial.extensions.git as git
import varial.extensions.make as make
import os

# varial.settings.use_parallel_chains = False

# dir_name = 'TpTpLooseSelection'
dir_name = 'TpTpControlRegion'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'

tc = varial.tools.ToolChain(
    dir_name,
    [
        make.Make([
           uhh_base + 'core',
           uhh_base + 'common',
           uhh_base + 'VLQSemiLepPreSel',
           uhh_base + 'VLQToHiggsPairProd',
        ]),
        # # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        git.GitAdder(),
        tight_sframe.sframe_tools_control_region,
        # loose_sframe.sframe_tools,
        # sensitivity.mk_tc(),
        git.GitTagger(),
        # varial.tools.WebCreator(no_tool_check=True), # no_tool_check=True
        # tex_content.tex_content,
        # varial.tools.CopyTool('~/www/test'),
    ]
)


# varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
varial.tools.Runner(tc, default_reuse=True)
# import varial.main
# varial.main.main(toolchain=tc, try_reuse_results=True)