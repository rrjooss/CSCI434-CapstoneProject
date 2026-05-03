import math
import sys

import numpy
import pandas
from matplotlib import pyplot
from sklearn.ensemble import ExtraTreesClassifier


def main():
    ts_df = pandas.read_csv("data/target_stats.csv").sample(frac=1)

    training_df = ts_df.iloc[0 : math.ceil(0.6 * len(ts_df))]

    dep = training_df["domain"]
    ind = training_df.drop("domain", axis=1).drop("url", axis=1)

    forest = ExtraTreesClassifier()
    forest.fit(ind, dep)

    feat_imp = forest.feature_importances_
    feat_imp_normalized = numpy.std(
        [tree.feature_importances_ for tree in forest.estimators_], axis=0
    )

    testing_df = ts_df.iloc[math.ceil(0.6 * len(ts_df)) : math.ceil(0.8 * len(ts_df))]

    test_ind = testing_df.drop("domain", axis=1).drop("url", axis=1)

    test_dep = training_df["domain"].tolist()
    test_pred = forest.predict(test_ind)

    print(test_dep)
    print(test_pred)

    pyplot.barh(ind.columns, feat_imp_normalized)
    pyplot.xlabel("Feature Importances")
    pyplot.ylabel("Feature Labels")
    pyplot.title("Comparison of different Feature Importances")

    pyplot.tight_layout()
    pyplot.savefig("plots/feature_importances.png")


if __name__ == "__main__":
    main()
