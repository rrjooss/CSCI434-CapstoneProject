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
        "time_delta": ["min", q1, "median", q3, "max", "mean", "std"],
        "pkt_len": ["min", q1, "median", q3, "max", "mean", "std"],
    }

    ts_df = lps_df.groupby("url").agg(aggregations)

    print(ts_df, file=sys.stderr)

    ts_df.columns = ["_".join(col).strip() for col in ts_df.columns.values]
    ts_df.rename(columns={"domain_first": "domain"}, inplace=True)

    ts_df_fin = ts_df.reset_index()

    ts_df_fin["pkt_count"] = ts_df_fin["url"].map(lps_df.groupby("url").size())

    print(ts_df_fin.columns, file=sys.stderr)

    ts_df_fin.to_csv("data/target_stats.csv", index=False)


if __name__ == "__main__":
    main()
