import sys
from collections import Counter

import numpy
import pandas
from matplotlib import pyplot


def q1(s):
    return s.quantile(0.25)


def q3(s):
    return s.quantile(0.75)


def main():

    lps_df = pandas.read_csv("data/labeled_pkt_stats.csv")

    aggregations = {
        "domain": "first",
        "time_delta": [q1, "median", q3, "max", "mean", "std"],
        "pkt_len": ["median", q3, "max", "mean", "std"],
    }

    ts_df = lps_df.groupby("url").agg(aggregations)

    print(ts_df, file=sys.stderr)

    ts_df.columns = ["_".join(col).strip() for col in ts_df.columns.values]

    ts_df_fin = ts_df.reset_index()
    ts_df_fin.rename(columns={"domain_first": "domain"}, inplace=True)

    ts_df_fin["pkt_count"] = ts_df_fin["url"].map(lps_df.groupby("url").size())

    print(ts_df_fin, file=sys.stderr)
    for column in ts_df_fin.columns:
        if ts_df_fin[column].nunique() == 1:
            print(f"{column} does not vary", file=sys.stderr)

    ts_df_fin.to_csv("data/target_stats.csv", index=False)


if __name__ == "__main__":
    main()
