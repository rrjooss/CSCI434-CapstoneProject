import sys

import numpy
import pandas


def main():

    intervals_df = pandas.read_csv("intervals.csv")
    pkt_stats_df = pandas.read_csv("pkt_stats.csv")

    print(intervals_df, file=sys.stderr)
    print(pkt_stats_df, file=sys.stderr)

    labeled_pkt_stats_df = pandas.DataFrame(
        columns=["domain", "url", "time_delta", "pkt_len"]
    )

    for interval in intervals_df.itertuples():
        new_target = True
        for pkt in pkt_stats_df.itertuples():
            if pkt.time_epoch > interval.end:
                break
            print(
                f"interval_idx = {interval.Index}, pkt_idx = {pkt.Index}, new_target = {new_target}",
                file=sys.stderr,
            )
            if pkt.time_epoch > interval.start and pkt.time_epoch < interval.end:
                labeled_pkt_stats_df.loc[len(labeled_pkt_stats_df)] = {
                    "domain": interval.domain,
                    "url": interval.url,
                    "time_delta": numpy.nan if new_target else pkt.time_delta,
                    "pkt_len": pkt.len,
                }
                new_target = False

    labeled_pkt_stats_df.to_csv("labeled_pkt_stats.csv", index=False)

    print(labeled_pkt_stats_df, file=sys.stderr)


if __name__ == "__main__":
    main()
