import common
import varial.tools
from varial.extensions.limits import *


tc = varial.tools.ToolChain(
    "Sensitivity",
    [
        varial.tools.HistoLoader(
            pattern='./*.root',
            filter_keyfunc=lambda w: 'EventHists/HT' in w.in_file_path and not
                ('AfterPresel' in w.in_file_path or 'Lep' in w.in_file_path),
            hook_loaded_histos=lambda w:
                common.add_wrp_info(
                w),
        ),
        # varial.tools.Plotter(
        #     plot_grouper=lambda w: (w,),
        #     save_name_func=lambda w: w._renderers[0].legend,
        # ),
        ThetaHistProducer(),
    ]
)
