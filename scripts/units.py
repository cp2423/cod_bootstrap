import pandas as pd

cwgc_csv = "/Users/chris/Dev/cod_records/cwgc/all_ww1_canadians.csv"

df = pd.read_csv(cwgc_csv)
uniq = df.Unit.unique()
out_df = pd.DataFrame(uniq, columns=["units"])
out_df.to_csv("units.csv", index=False)