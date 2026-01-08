def process_csv_files(model_ws="."):
    import os
    import pandas as pd
    import flopy

    sim = flopy.mf6.MFSimulation.load(sim_ws=model_ws, load_only=["tdis"])
    start = pd.to_datetime(sim.tdis.start_date_time.data)
    csv_files = [f for f in os.listdir(model_ws) if f.endswith(".csv")]
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
