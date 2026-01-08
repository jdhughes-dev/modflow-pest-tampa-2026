import os
import pandas as pd
import flopy


def process_csv_files(model_ws="."):
    import os
    import pandas as pd

    sim = flopy.mf6.MFSimulation.load(sim_ws=model_ws, load_only=["tdis"])
    start = pd.to_datetime(sim.tdis.start_date_time.data)
    csv_files = [f for f in os.listdir(model_ws) if f.endswith(".csv")]
    aq_df = None
    wt_df = None
    for csv_file in csv_files:
        try:
            df = pd.read_csv(os.path.join(model_ws, csv_file))
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
        print(csv_file)
        if "sv.gwf.wt.csv" in csv_file:
            wt_df = df
        elif "sv.gwf.aq.csv" in csv_file:
            aq_df = df
    if aq_df is not None and wt_df is not None:
        print(wt_df)
        print(aq_df)
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


if __name__ == "__main__":
    extract_true_obs(
        os.path.join("..", "models", "synthetic-valley-truth-advanced-monthly")
    )
