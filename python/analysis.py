#!/usr/bin/env python


# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as common
import sframe_tools
import sensitivity
# import tex_content

import varial.tools
import os

# varial.settings.use_parallel_chains = False


dir_name = 'TpTpTightSelection_output2'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'


tc = varial.tools.ToolChain(
    dir_name,
    [
        varial.tools.CompileTool([
           uhh_base + 'core',
           uhh_base + 'common',
           uhh_base + 'VLQSemiLepPreSel',
           uhh_base + 'VLQToHiggsPairProd',
        ]),
        varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        sframe_tools.sframe_tools,
        # sensitivity.tc,
        # varial.tools.PrintToolTree(),
        varial.tools.WebCreator(no_tool_check=True),
        # tex_content.tex_content,
        # varial.tools.CopyTool('~/www/test'),
    ]
)


# varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
# varial.tools.Runner(tc, True)
import varial.main
varial.main.main(toolchain=tc, try_reuse_results=True)