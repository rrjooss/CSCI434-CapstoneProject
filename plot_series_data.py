import sys
from collections import Counter

import numpy
import pandas
from matplotlib import pyplot


def main():

    lps_df = pandas.read_csv("data/labeled_pkt_stats.csv")

    domains = lps_df["domain"].unique()

    lps_by_domain_dfs = map(lambda domain: lps_df[lps_df["domain"] == domain], domains)

    lps_df.plot.hist(
        column=["pkt_len"],
        by="domain",
        bins=1000,
        figsize=(10, 8),
        log=True,
    )

    pyplot.tight_layout()
    pyplot.savefig("plots/pkt_len_distribution.png")

    lps_df.plot.hist(
        column=["time_delta"],
        by="domain",
        bins=1000,
        figsize=(10, 8),
        log=True,
    )

    pyplot.tight_layout()
    pyplot.savefig("plots/time_delta_distribution.png")


if __name__ == "__main__":
    main()
