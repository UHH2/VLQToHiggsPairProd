import varial.tools
import varial.generators as gen
import normplots
import common_sensitivity
import common_vlq
import varial.operations as op
import varial.analysis

cat_colors = [
    632,
    902,
    840,
    434,
    870,
]

def select_files(wrp):
    if ((wrp.in_file_path == 'PostSelection/ST'
        or wrp.in_file_path == 'PostSelection/leading_jet_pt'
        or wrp.in_file_path == 'PostSelection/pt_ld_patJetsAk8CHSJetsSoftDropPacked_daughters'
        )
        and 'MC' in wrp.file_path
        and '1HiggsLooseTagSignalRegion' not in wrp.file_path
        ):
        return True


def colorize_signal_region(wrp):
    wrp.obj.SetFillColor(varial.ROOT.kGray)
    wrp.obj.SetLineColor(varial.ROOT.kBlack)
    wrp.obj.SetLineWidth(1)
    return wrp

def set_linewidth_others(wrps):
    for wrp in wrps:
        wrp.obj.SetLineWidth(2)
    return wrps


def plot_setup(grps):
    for grp in grps:
        grp = list(grp)
        dat, bkg, sig = gen.split_data_bkg_sig(grp)
        dat, bkg, sig = list(dat), list(bkg), list(sig)
        # print 'SELECTED SAMPLES: ', bkg, sig
        if bkg:
            selected_smpls = bkg
        else:
            selected_smpls = sig
        signal = filter(lambda w: '1HiggsMedTagSignalRegion' == w.legend, selected_smpls)
        others = filter(lambda w: '1HiggsMedTagSignalRegion' != w.legend, selected_smpls)
        if not signal:
            yield others + dat
        colorize_signal_region(signal[0])
        set_linewidth_others(others)
        signal = [op.stack(signal)]
        if dat:
            dat = [op.norm_to_integral(varial.op.merge(dat))]
        yield signal + others + dat


def plot_colorizer(grps, colors=cat_colors):
    grps = (gen.apply_linecolor(ws, colors) for ws in grps)
    # grps = (gen.apply_fillcolor(ws, colors) for ws in grps
    #     if ws.category == '1HiggsMedTagSignalRegion')
    grps = (gen.apply_markercolor(ws, colors) for ws in grps)
    return grps


def loader_hook(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    # wrps = add_cat_info(wrps)
    wrps = gen.gen_add_wrp_info(
        wrps, category=lambda w: w.file_path.split('/')[-3])
        # legend=lambda w: w.file_path.split('/')[-3])
    wrps = gen.sort(wrps, key_list=['category'])
    wrps = common_vlq.merge_samples(wrps)
    wrps = gen.sort(wrps, key_list=['sample', 'in_file_path'])
    wrps = gen.gen_add_wrp_info(
        wrps, legend=lambda w: w.category,
        draw_option=lambda w: 'hist' if not w.is_data else 'E1X0')
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = common_vlq.label_axes(wrps)

    # wrps = gen.switch(
    #     wrps,
    #     lambda w: w.in_file_path.split('/')[0] == 'GenHists',
    #     gen.gen_make_th2_projections
    # )
    # wrps = gen.gen_make_eff_graphs(wrps)
    wrps = gen.gen_norm_to_integral(wrps)
    return wrps

def mk_tc():
    # return varial.tools.ToolChain('CompareControlRegion',
    return [
        varial.tools.HistoLoader(
            # name='HistoLoaderSplit'+str(ind),
            # pattern=file_stack_split(),
            filter_keyfunc=select_files,
            hook_loaded_histos=loader_hook
            ),
        varial.tools.Plotter(
            input_result_path='../HistoLoader',
            # load_func=gen_apply_legend(
            #         gen.load(gen.fs_content())),
            # combine_files=True,
            plot_grouper=lambda ws: gen.group(
                ws, key_func=lambda w: w.sample and w.in_file_path),
            plot_setup=lambda w: plot_setup(plot_colorizer(w)),
            save_name_func=lambda w: w.sample+'_'+w.name,
            canvas_decorators=[varial.rendering.Legend]
            )
        ]
        # )