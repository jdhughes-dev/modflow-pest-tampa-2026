import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pyemu


def process_csv_files(model_ws="."):
    import os
    import pandas as pd
    import flopy

    sim = flopy.mf6.MFSimulation.load(sim_ws=model_ws, load_only=["tdis"])
    start = pd.to_datetime(sim.tdis.start_date_time.data)
    csv_files = [f for f in os.listdir(model_ws) if f.endswith(".csv")]
    aq_df = None
    wt_df = None
    swgw_dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(os.path.join(model_ws, csv_file), low_memory=True)
        except Exception:
            continue
        df.columns = df.columns.map(
            lambda x: x.lower().replace("_", "-").replace("(", "-").replace(")", "-")
        )
        if "time" in df.columns:
            df.index = start + pd.to_timedelta(
                df.pop("time").astype(float).values, unit="d"
            )
            df.index.name = "datetime"
            df.to_csv(os.path.join(model_ws, csv_file))
        # print(csv_file)
        if "sv.gwf.wt.csv" in csv_file:
            wt_df = df
        elif "sv.gwf.aq.csv" in csv_file:
            aq_df = df
        swgw_df = df.loc[
            :,
            (df.columns.str.contains("riv-swgw"))
            | (df.columns.str.contains("lake-stage")),
        ]
        # print(csv_file,swgw_df.shape)
        if swgw_df.shape[1] > 0 and csv_file.startswith("sv"):
            if "datetime" in df.columns:
                swgw_df.index = pd.to_datetime(df.datetime)
            # print(swgw_df)
            print("found", csv_file)
            # if rivswgw_df is not None:
            #    raise Exception("#shitsbusted")
            swgw_dfs.append(swgw_df)

    if swgw_dfs is not None:
        df = pd.concat(swgw_dfs, axis=1)
        hist_mean = df.loc[df.index.year < 2015, :].mean()
        pred_mean = df.loc[df.index.year >= 2015, :].mean()
        diff_mean = hist_mean - pred_mean
        df = pd.DataFrame(
            data={
                "hist-mean": hist_mean,
                "pred-mean": pred_mean,
                "diff-mean": diff_mean,
            }
        )
        df.index.name = "quantity"
        df.to_csv(os.path.join(model_ws, "swgw-longterm-means.csv"))

    if aq_df is not None and wt_df is not None:
        # print(wt_df)
        # print(aq_df)
        if "datetime" in wt_df.columns:
            wt_df.index = pd.to_datetime(wt_df.pop("datetime"))
        if "datetime" in aq_df.columns:
            aq_df.index = pd.to_datetime(aq_df.pop("datetime"))
        aq_df.sort_index(inplace=True)
        aq_df.sort_index(inplace=True, axis=1)
        wt_df.sort_index(inplace=True)
        wt_df.sort_index(inplace=True, axis=1)

        cnames = [c.replace("aq", "diff") for c in aq_df.columns]
        diff_df = pd.DataFrame(
            data=wt_df.values - aq_df.values, index=wt_df.index, columns=cnames
        )
        diff_df.index.name = "datetime"
        diff_df.to_csv(os.path.join(model_ws, "sv.gwf.diff.csv"))


def extract_true_obs(m_d):
    process_csv_files(m_d)
    ofiles = [
        "sv.lake.obs.csv",
        "sv.sfr.obs.csv",
        "sv.gwf.wt.csv",
        "sv.gwf.scenario.csv",
        "sv.gwf.aq.csv",
        "sv.gwf.diff.csv",
    ]

    dfs = [pd.read_csv(os.path.join(m_d, ofile), index_col=0) for ofile in ofiles]
    df = pd.concat(dfs, axis=1)
    # df.index = pd.to_datetime(sim.tdis.start_date_time.data) + pd.to_timedelta(np.cumsum(perlen),unit="d")
    df.columns = df.columns.map(str.lower)
    df.to_csv(os.path.join(m_d, "raw_obs.csv"))
    print(df)


def plot_ies_properties(m_d, tag, noptmax=None):
    pst = pyemu.Pst(os.path.join(m_d, "pest.pst"))
    obs = pst.observation_data
    tobs = obs.loc[obs.obsnme.str.contains(tag), :].copy()
    assert len(tobs) > 0
    tobs["i"] = tobs.i.astype(int)
    tobs["j"] = tobs.j.astype(int)
    nrow = tobs.i.max() + 1
    ncol = tobs.j.max() + 1

    pr = pst.ies.obsen0
    pt = None
    num_reals = 3
    if noptmax != 0 and pst.ies.phiactual.iteration.max() > 0:
        if noptmax is None:
            noptmax = pst.ies.phiactual.iteration.max()
        pt = pst.ies.get("obsen", noptmax)
        fig, axes = plt.subplots(2, num_reals, figsize=(12, 10))
    else:
        fig, axes = plt.subplots(1, num_reals, figsize=(10, 4))
        axes = np.atleast_2d(axes)

    real_names = []
    if "base" in pr.index:
        if pt is not None:
            if "base" in pt.index:
                real_names.append("base")
        else:
            real_names.append("base")
    for i in range(len(real_names), num_reals):
        if pt is not None:
            real_names.append(pt.index[i])
        else:
            real_names.append(pr.index[i])

    pr = pr.loc[real_names, tobs.obsnme].apply(np.log10)
    vmin = pr.values.min()
    vmax = pr.values.max()
    if pt is not None:
        pt = pt.loc[real_names, tobs.obsnme].apply(np.log10)
        vmin = max(vmin, pt.values.min())
        vmax = max(vmax, pt.values.max())

    # axes = axes.flatten()
    ax_count = 0

    for i, real_name in enumerate(real_names):
        ax = axes[0, i]
        vals = np.zeros((nrow, ncol))
        vals[tobs.i, tobs.j] = pr.loc[real_name, tobs.obsnme]
        # print(pr.loc[real_name,tobs.obsnme])

        cb = ax.imshow(vals, vmin=vmin, vmax=vmax)

        plt.colorbar(cb, ax=ax, label="log10")
        # plt.show()
        # exit()
        ax.set_title("{1} real:{0} prior".format(real_name, tag), loc="left")
        ax.set_aspect("equal")
        ax.set_yticks([])
        ax.set_xticks([])
        ax_count += 1

        if pt is not None:
            ax = axes[1, i]
            vals = np.zeros((nrow, ncol))
            vals[tobs.i, tobs.j] = pt.loc[real_name, tobs.obsnme]
            cb = ax.imshow(vals, vmin=vmin, vmax=vmax)
            plt.colorbar(cb, ax=ax, label="log10")
            ax.set_title("{1} real:{0} post".format(real_name, tag), loc="left")
            ax.set_aspect("equal")
            ax.set_yticks([])
            ax.set_xticks([])
            ax_count += 1

    plt.tight_layout()
    # plt.show()
    # plt.savefig("test.pdf")
    # plt.close(fig)
    return fig, axes


def plot_ies_timeseries(m_d, noptmax=None):
    truth_obs = pd.read_csv(
        os.path.join(
            "..", "models", "synthetic-valley-truth-advanced-monthly", "raw_obs.csv"
        ),
        index_col=0,
        parse_dates=True,
    )
    pst = pyemu.Pst(os.path.join(m_d, "pest.pst"))
    obs = pst.observation_data
    sgobs = obs.loc[pd.notna(obs.usecol), :]
    sgobs = sgobs.loc[sgobs.usecol.str.contains("swgw"), :].copy()
    sgobs["datetime"] = pd.to_datetime(sgobs.datetime)
    sg_grps = sgobs.obgnme.unique()
    sg_grps.sort()
    # print(sg_grps)
    # exit()

    lkobs = obs.loc[obs.usecol == "lake-stage", :].copy()
    lkobs["datetime"] = pd.to_datetime(lkobs.datetime)
    lkobs.sort_values(by="datetime", inplace=True)

    rfobs = obs.loc[obs.obsnme.str.contains("riv-flow"), :].copy()
    rfobs["datetime"] = pd.to_datetime(rfobs.datetime)
    rfobs.sort_values(by="datetime", inplace=True)

    nz_grps = obs.loc[obs.weight > 0, "obgnme"].unique()
    nz_grps.sort()
    grps = obs.obgnme.unique()
    assert len(nz_grps) > 0
    aq_grps = [g for g in nz_grps if "aq" in g]
    assert len(aq_grps) > 0
    wt_grps = [g.replace("aq", "wt") for g in aq_grps]
    for g in wt_grps:
        assert g in nz_grps
    dif_grps = [g.replace("aq", "diff") for g in aq_grps]
    for g in dif_grps:
        assert g in grps

    # print(nz_grps)

    pr = pst.ies.obsen0
    noise = pst.ies.noise
    pt = None
    if noptmax != 0 and pst.ies.phiactual.iteration.max() > 0:
        if noptmax is None:
            noptmax = pst.ies.phiactual.iteration.max()
        pt = pst.ies.get("obsen", noptmax)

    with PdfPages(os.path.join(m_d, "timeseries.pdf")) as pdf:
        fig, axes = plt.subplots(len(sg_grps), 1, figsize=(10, 5 * len(sg_grps)))
        if len(sg_grps) == 1:
            axes = [axes]
        for ax, grp in zip(axes, sg_grps):
            oobs = sgobs.loc[sgobs.obgnme == grp, :].copy()
            oobs.sort_values(by="datetime", inplace=True)

            dts = oobs.datetime.values
            vals = pr.loc[:, oobs.obsnme].values
            [
                ax.plot(dts, vals[i, :], "0.5", lw=0.1, alpha=0.2)
                for i in range(vals.shape[0])
            ]
            ax.plot(dts, vals[-1, :], "0.5", lw=0.1, label="prior")
            nzobs = oobs.loc[oobs.weight > 0, :].copy()
            nzdts = nzobs.datetime.values
            vals = noise.loc[:, nzobs.obsnme].values
            [
                ax.plot(nzdts, vals[i, :], "r", lw=0.1, alpha=0.2)
                for i in range(vals.shape[0])
            ]
            ax.plot(nzdts, vals[-1, :], "r", lw=0.1, label="obs+noise")
            ax.scatter(
                nzdts, nzobs.obsval, marker="^", s=50, c="r", zorder=10, label="obs"
            )
            if pt is not None:
                vals = pt.loc[:, oobs.obsnme].values
                [
                    ax.plot(dts, vals[i, :], "b", lw=0.2, alpha=0.5)
                    for i in range(vals.shape[0])
                ]
                ax.plot(dts, vals[-1, :], "b", lw=0.2, label="posterior")
            # ax.plot(dts, oobs.obsval, "r--", lw=2, label="truth")
            usecol = oobs.usecol.unique()
            tobs = truth_obs.loc[:, usecol]
            ax.plot(tobs.index, tobs.values, "k--", lw=2, label="truth", zorder=10)
            ax.set_title(grp, loc="left")
            ax.legend(loc="upper right")
            ax.grid()
        plt.tight_layout()
        pdf.savefig()
        plt.close(fig)

        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        oobs = lkobs
        oobs.sort_values(by="datetime", inplace=True)
        dts = oobs.datetime.values
        vals = pr.loc[:, oobs.obsnme].values
        [
            ax.plot(dts, vals[i, :], "0.5", lw=0.1, alpha=0.2)
            for i in range(vals.shape[0])
        ]
        ax.plot(dts, vals[-1, :], "0.5", lw=0.1, label="prior")
        nzobs = oobs.loc[oobs.weight > 0, :].copy()
        nzdts = nzobs.datetime.values
        vals = noise.loc[:, nzobs.obsnme].values
        [
            ax.plot(nzdts, vals[i, :], "r", lw=0.1, alpha=0.2)
            for i in range(vals.shape[0])
        ]
        ax.plot(nzdts, vals[-1, :], "r", lw=0.1, label="obs+noise")
        ax.scatter(nzdts, nzobs.obsval, marker="^", s=50, c="r", zorder=10, label="obs")
        if pt is not None:
            vals = pt.loc[:, oobs.obsnme].values
            [
                ax.plot(dts, vals[i, :], "b", lw=0.2, alpha=0.5)
                for i in range(vals.shape[0])
            ]
            ax.plot(dts, vals[-1, :], "b", lw=0.2, label="posterior")
        # ax.plot(dts, oobs.obsval, "r--", lw=2, label="truth")
        usecol = oobs.usecol.unique()
        tobs = truth_obs.loc[:, usecol]
        ax.plot(tobs.index, tobs.values, "k--", lw=2, label="truth", zorder=10)
        ax.set_title("lake-stage", loc="left")
        ax.legend(loc="upper right")
        ax.grid()
        plt.tight_layout()
        pdf.savefig()
        plt.close(fig)

        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        oobs = rfobs
        oobs.sort_values(by="datetime", inplace=True)
        dts = oobs.datetime.values
        vals = pr.loc[:, oobs.obsnme].values
        [
            ax.plot(dts, vals[i, :], "0.5", lw=0.1, alpha=0.2)
            for i in range(vals.shape[0])
        ]
        ax.plot(dts, vals[-1, :], "0.5", lw=0.1, label="prior")
        nzobs = oobs.loc[oobs.weight > 0, :].copy()
        nzdts = nzobs.datetime.values
        vals = noise.loc[:, nzobs.obsnme].values
        [
            ax.plot(nzdts, vals[i, :], "r", lw=0.1, alpha=0.2)
            for i in range(vals.shape[0])
        ]
        ax.plot(nzdts, vals[-1, :], "r", lw=0.1, label="obs+noise")
        ax.scatter(nzdts, nzobs.obsval, marker="^", s=50, c="r", zorder=10, label="obs")
        if pt is not None:
            vals = pt.loc[:, oobs.obsnme].values
            [
                ax.plot(dts, vals[i, :], "b", lw=0.2, alpha=0.5)
                for i in range(vals.shape[0])
            ]
            ax.plot(dts, vals[-1, :], "b", lw=0.2, label="posterior")
        # ax.plot(dts, oobs.obsval, "r--", lw=2, label="truth")
        usecol = oobs.usecol.unique()
        tobs = truth_obs.loc[:, usecol]
        ax.plot(tobs.index, tobs.values, "k--", lw=2, label="truth", zorder=10)
        ax.set_title("riv-flow", loc="left")
        ax.legend(loc="upper right")
        ax.grid()
        plt.tight_layout()
        pdf.savefig()
        plt.close(fig)

        for agrp, wgrp, dgrp in zip(aq_grps, wt_grps, dif_grps):
            aobs = obs.loc[obs.obgnme == agrp, :].copy()
            aobs["datetime"] = pd.to_datetime(aobs.datetime)
            aobs.sort_values(by="datetime", inplace=True)

            wobs = obs.loc[obs.obgnme == wgrp, :].copy()
            wobs["datetime"] = pd.to_datetime(wobs.datetime)
            wobs.sort_values(by="datetime", inplace=True)
            dobs = obs.loc[obs.obgnme == dgrp, :].copy()
            dobs["datetime"] = pd.to_datetime(dobs.datetime)
            dobs.sort_values(by="datetime", inplace=True)

            fig, axes = plt.subplots(3, 1, figsize=(10, 10))
            for ax, oobs, grp in zip(axes, [wobs, aobs, dobs], [wgrp, agrp, dgrp]):
                dts = oobs.datetime.values

                nzobs = oobs.loc[oobs.weight > 0, :].copy()
                nzdts = nzobs.datetime.values
                vals = noise.loc[:, nzobs.obsnme].values
                [
                    ax.plot(nzdts, vals[i, :], "r", lw=0.1, alpha=0.2)
                    for i in range(vals.shape[0])
                ]
                ax.plot(nzdts, vals[-1, :], "r", lw=0.1, label="obs+noise")
                ax.scatter(
                    nzdts, nzobs.obsval, marker="^", s=50, c="r", zorder=10, label="obs"
                )
                if pt is not None:
                    vals = pt.loc[:, oobs.obsnme].values
                    [
                        ax.plot(dts, vals[i, :], "b", lw=0.2, alpha=0.5)
                        for i in range(vals.shape[0])
                    ]
                    ax.plot(dts, vals[-1, :], "b", lw=0.2, label="posterior")
                # ax.plot(dts, oobs.obsval, "r--", lw=2, label="truth")
                usecol = oobs.usecol.unique()
                tobs = truth_obs.loc[:, usecol]
                ax.plot(tobs.index, tobs.values, "k--", lw=2, label="truth", zorder=10)
                ylim = ax.get_ylim()
                vals = pr.loc[:, oobs.obsnme].values
                [
                    ax.plot(dts, vals[i, :], "0.5", lw=0.1, alpha=0.2)
                    for i in range(vals.shape[0])
                ]
                ax.plot(dts, vals[-1, :], "0.5", lw=0.1, label="prior")
                ax.set_ylim(ylim)
                ax.set_title(grp, loc="left")
                ax.legend(loc="upper right")
                ax.grid()
            plt.tight_layout()
            pdf.savefig()
            plt.close(fig)


def plot_ies_forecasts(m_d, noptmax=None):
    pst = pyemu.Pst(os.path.join(m_d, "pest.pst"))
    obs = pst.observation_data
    fobs = obs.loc[obs.oname == "forecasts", :]
    assert len(fobs) > 0
    quans = fobs.quantity.unique()
    quans.sort()
    # print(quans)

    pr = pst.ies.obsen0
    pt = None
    if noptmax != 0 and pst.ies.phiactual.iteration.max() > 0:
        if noptmax is None:
            noptmax = pst.ies.phiactual.iteration.max()
        pt = pst.ies.get("obsen", noptmax)

    usecol_order = ["hist-mean", "pred-mean", "diff-mean"]
    for u in usecol_order:
        assert u in fobs.usecol.unique()
    figs, axess = [], []
    with PdfPages(os.path.join(m_d, "forecasts.pdf")) as pdf:
        for quan in quans:
            uobs = fobs.loc[fobs.quantity == quan, :]
            uobs.sort_index(inplace=True)

            fig, axes = plt.subplots(len(uobs), 1, figsize=(8, 2 * len(uobs)))
            if len(uobs) == 1:
                axes = [axes]
            for ax, usecol in zip(axes, usecol_order):
                oname = uobs.loc[uobs.usecol == usecol, "obsnme"]

                if pt is not None:
                    ax.hist(
                        pt.loc[:, oname].values,
                        bins=20,
                        fc="b",
                        alpha=0.5,
                        label="posterior",
                    )

                ax.set_title("{0} {1}".format(quan, usecol), loc="left")
                # xlim = ax.get_xlim()
                ax.hist(
                    pr.loc[:, oname].values, bins=20, fc="0.5", alpha=0.5, label="prior"
                )
                # ax.set_xlim(xlim)
                tval = uobs.loc[oname, "obsval"]
                # print(quan,usecol,tval)
                ax.plot(
                    [tval, tval], ax.get_ylim(), "k--", lw=2, label="truth", zorder=10
                )
                ax.legend(loc="upper right")
                ax.set_yticks([])
                ax.grid("off")
            mx = max([ax.get_xlim()[1] for ax in axes[:-1]])
            mn = min([ax.get_xlim()[0] for ax in axes[:-1]])
            axes[0].set_xlim(mn, mx)
            axes[1].set_xlim(mn, mx)

            plt.tight_layout()
            pdf.savefig()
            # plt.close(fig)
            figs.append(fig)
            axess.append(axes)
        return figs, axes


if __name__ == "__main__":
    # process_csv_files(os.path.join("..","models","synthetic-valley-truth-advanced-monthly"))
    # extract_true_obs(
    #    os.path.join("..", "models", "synthetic-valley-truth-advanced-monthly")
    # )
    # fig,axes = plot_ies_properties("master_ies_advanced","sto-ss-layer1",noptmax=None)
    # plt.savefig("test.pdf")
    # plt.close(fig)
    # plot_ies_timeseries("master_ies_base_mm", noptmax=None)
    plot_ies_forecasts("master_ies_base_mm", noptmax=None)
