#!/usr/bin/env python

import common
import settings
import plot_stks
import sensitivity

import varial.main
import varial.tools

tc = varial.tools.ToolChain('Main', [
    #plot_stks.p,
    sensitivity.tc,
    varial.tools.WebCreator(),
    varial.tools.CopyTool('~/www/test'),
])

varial.analysis.fs_aliases = varial.diskio.generate_aliases()
varial.main.main(toolchain=tc)