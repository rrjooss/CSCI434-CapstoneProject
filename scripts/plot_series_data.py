import sys
from collections import Counter

import numpy
import pandas
from matplotlib import pyplot


def main():

    lps_df = pandas.read_csv("data/labeled_pkt_stats.csv")

    for col in ["pkt_len", "time_delta"]:
        lps_df.plot.hist(
            column=[col],
            by="domain",
            bins=1000,
            figsize=(10, 8),
            log=True,
        )

        pyplot.tight_layout()
        pyplot.savefig(f"plots/{col}_distribution.png")

    ts_df = pandas.read_csv("data/target_stats.csv")

    for col in [
        "time_delta_q1",
        "time_delta_median",
        "time_delta_q3",
        "time_delta_max",
        "time_delta_mean",
        "time_delta_std",
        "pkt_len_median",
        "pkt_len_q3",
        "pkt_len_max",
        "pkt_len_mean",
        "pkt_len_std",
    ]:
        ts_df.plot.hist(
            column=[col],
            by="domain",
            bins=100,
            figsize=(10, 8),
        )

        pyplot.tight_layout()
        pyplot.savefig(f"plots/{col}_distribution.png")


if __name__ == "__main__":
    main()
