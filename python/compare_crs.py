import varial.tools
import varial.generators as gen
import normplots
import common_sensitivity
import common_vlq
# import tight_sframe
import varial.operations as op
import varial.analysis
import varial.rendering

cat_colors = [
    632,
    902,
    840,
    434,
    870,
]

class BottomPlotControlSignalRatio(varial.rendering.BottomPlotRatio):
    """Same as BottomPlotRatio, but split MC and data uncertainties."""

    def check_renderers(self):
        n_hists = len(self.renderers)

        # if 'TH2' in self.renderers[0].type:
        #     return False

        if n_hists != 2:
            raise RuntimeError('ERROR BottomPlots can only be created '
                               'with exactly two histograms!')
        return n_hists == 2

    def define_bottom_hist(self):
        rnds = self.renderers
        sr_histo = rnds[0].histo.Clone()
        cr_histo = filter(lambda r: r.category == self.dec_par['div_category'],
                          rnds)[0].histo.Clone()
        div_hist = cr_histo.Clone()
        div_hist.Divide(sr_histo)
        for i in xrange(1, sr_histo.GetNbinsX() + 1):
            mc_val  = sr_histo.GetBinContent(i)
            mc_err  = sr_histo.GetBinError(i)
            da_val  = cr_histo.GetBinContent(i)
            da_err  = cr_histo.GetBinError(i)
            div_val = div_hist.GetBinContent(i)
            sr_histo.SetBinContent(i, 0.)
            if mc_val > 1e-37:
                sr_histo.SetBinError(i, mc_err / mc_val)
                div_hist.SetBinContent(i, div_val - 1.)
            else:
                sr_histo.SetBinError(i, 0.)
            if da_val > 1e-37:
                div_hist.SetBinError(i, da_err * div_val / da_val)
        div_hist.SetYTitle(self.dec_par['y_title'])
        div_hist.SetMarkerSize(0)
        sr_histo.SetYTitle(self.dec_par['y_title'])
        sr_histo.SetFillColor(921)
        sr_histo.SetMarkerColor(1)
        sr_histo.SetMarkerSize(0)
        sr_histo.SetFillStyle(3008)
        sr_histo.SetLineColor(1)
        self.bottom_hist = div_hist
        self.bottom_hist_mc_err = sr_histo

    def draw_full_plot(self):
        """Draw mc error histo below data ratio."""
        super(BottomPlotControlSignalRatio, self).draw_full_plot()
        if not self.dec_par['renderers_check_ok']:
            return
        self.second_pad.cd()
        self.bottom_hist_mc_err.Draw('sameE2')
        self.bottom_hist.Draw(self.dec_par['draw_opt'] + 'same')
        self.main_pad.cd()

def select_files(wrp):
    if ((wrp.in_file_path.endswith('PostSelection/ST')
            or wrp.in_file_path.endswith('PostSelection/leading_jet_pt')
            or wrp.in_file_path.endswith('PostSelection/met')
            or wrp.in_file_path.endswith('PostSelection/primary_lepton_pt')
            or wrp.in_file_path.endswith('PostSelection/pt_ld_patJetsAk8CHSJetsSoftDropPacked_daughters')
            or wrp.in_file_path.endswith('PostSelection/n_jets')
            or wrp.in_file_path.endswith('PostSelection/n_patJetsAk8CHSJetsSoftDropPacked_daughters')
            )
            and 'MC.TTbar' in wrp.file_path
            # and '1HiggsLooseTagSignalRegion' not in wrp.file_path
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


def overlay_setup(grps, sig_reg=''):
    for grp in grps:
        print sig_reg
        grp = list(grp)
        dat, bkg, sig = gen.split_data_bkg_sig(grp)
        dat, bkg, sig = list(dat), list(bkg), list(sig)
        # print 'SELECTED SAMPLES: ', bkg, sig
        if bkg:
            selected_smpls = bkg
        else:
            selected_smpls = sig
        signal = filter(lambda w: sig_reg == w.legend, selected_smpls)
        others = filter(lambda w: sig_reg != w.legend, selected_smpls)
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
    grps = (gen.apply_markercolor(ws, colors) for ws in grps)
    return grps

def plot_setup(sig_reg=''):
    def setup(grps):
        grps = plot_colorizer(grps)
        grps = overlay_setup(grps, sig_reg)
        return grps
    return setup


def loader_hook(wrps):
    wrps = common_vlq.add_wrp_info(wrps)
    # wrps = add_cat_info(wrps)
    wrps = gen.gen_add_wrp_info(
        wrps, category=lambda w: w.in_file_path.split('/')[0],
        variable=lambda w: w.in_file_path.split('/')[-1])
        # legend=lambda w: w.file_path.split('/')[-3])
    wrps = gen.sort(wrps, key_list=['category'])
    wrps = common_vlq.merge_samples(wrps)
    wrps = gen.sort(wrps, key_list=['sample', 'variable'])
    # wrps = list(wrps)
    # for w in wrps:
    #     print w.sample, w.in_file_path
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

# CONTINUE HERE WITH FILTERING!!

def filter_category(sig_cats=None, sig_cat='', cr_cat=''):
    def do_filtering(wrp):
        if (cr_cat and (wrp.category == cr_cat or wrp.category == sig_cat))\
            or (not cr_cat and (wrp.category == sig_cat or wrp.category not in sig_cats)):
            # print wrp.category
            return True
        else: return False
    return do_filtering

def make_bottom_plot(cat=''):
    def return_bottom_plot_class(target, **kws):
        return BottomPlotControlSignalRatio(target, dd=True, div_category=cat, **kws)
    return return_bottom_plot_class

def mk_tc(srs=None, crs=None):
    def create():
        # return varial.tools.ToolChain('CompareControlRegion',
        tc = []
        for sig in srs:
            sig_tc = [
            varial.tools.HistoLoader(
                # name='HistoLoaderSplit'+str(ind),
                # pattern=file_stack_split(),
                filter_keyfunc=select_files,
                hook_loaded_histos=loader_hook
                ),
            varial.tools.Plotter(
                name='AllCategories',
                input_result_path='../HistoLoader',
                # load_func=gen_apply_legend(
                #         gen.load(gen.fs_content())),
                # combine_files=True,
                filter_keyfunc=filter_category(srs, sig),
                plot_grouper=lambda ws: gen.group(
                    ws, key_func=lambda w: w.sample and w.variable),
                plot_setup=plot_setup(sig),
                save_name_func=lambda w: w.sample+'_'+w.name,
                canvas_decorators=[varial.rendering.Legend]
                )
            ]
            for cr in crs:
                sig_tc.append(varial.tools.Plotter(
                    name=cr,
                    input_result_path='../HistoLoader',
                    filter_keyfunc=filter_category(srs, sig, cr),
                    plot_grouper=lambda ws: gen.group(
                        ws, key_func=lambda w: w.sample and w.variable),
                    plot_setup=plot_setup(sig),
                    save_name_func=lambda w: w.sample+'_'+w.name,
                    save_lin_log_scale=True,
                    canvas_decorators=[
                    make_bottom_plot(cr),
                    varial.rendering.Legend]
                    ))
            tc.append(varial.tools.ToolChain(sig, sig_tc))
        return tc
    return create
        # )