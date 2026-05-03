import math
import sys

import numpy
import pandas
import seaborn
from matplotlib import pyplot
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def fmt_props_head(s):
    return ", ".join(
        [key for key, value in s.value_counts(normalize=True).to_dict().items()]
    )


def fmt_props(s):
    return ", ".join(
        [
            f"{value*110:.1f}%"
            for key, value in s.value_counts(normalize=True).to_dict().items()
        ]
    )


def fmt_splits(label, X, y, original):
    return f"{f'{label}:':<11} {len(X):<3} ({len(X)/len(original)*100:5.1f}%); {fmt_props(y)}"


def main():
    ts_df = pandas.read_csv("data/target_stats.csv").sample(frac=1)

    target_col = "domain"
    feature_cols = [col for col in ts_df.columns if col not in ["url", "domain"]]

    X = ts_df[feature_cols]
    y = ts_df[target_col]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print(f"Classes found: {label_encoder.classes_}")
    print(f"Number of classes: {len(label_encoder.classes_)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=3, stratify=y_encoded
    )

    print(f"\nData Split Sizes and Distributions ({fmt_props_head(ts_df['domain'])}):")
    print(fmt_splits("Original", ts_df, ts_df["domain"], ts_df))
    print(fmt_splits("Training", X_train, pandas.Series(y_train), ts_df))
    print(fmt_splits("Test", X_test, pandas.Series(y_test), ts_df))

    forest = ExtraTreesClassifier(bootstrap=True, random_state=42)
    forest.fit(X_train, y_train)

    test_preds = forest.predict(X_test)

    test_acc = accuracy_score(y_test, test_preds)

    print(f"\nModel Performance:")
    print(f"Test Accuracy: {test_acc:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(y_test, test_preds, target_names=label_encoder.classes_)
    )

    feature_importances = forest.feature_importances_
    feat_imp_df = pandas.DataFrame(
        {"Feature": feature_cols, "Importance": feature_importances}
    ).sort_values(by="Importance", ascending=False)

    print("\nTop 5 Most Important Features:")
    print(feat_imp_df.head())

    pyplot.style.use("seaborn-v0_8-whitegrid")
    fig, axs = pyplot.subplots(1, 2, figsize=(18, 6))

    axs[0].barh(feat_imp_df["Feature"], feat_imp_df["Importance"], color="skyblue")
    axs[0].set_xlabel("Importance Score")
    axs[0].set_title("Feature Importances")
    axs[0].invert_yaxis()  # Highest importance at top

    cm = confusion_matrix(y_test, test_preds)
    seaborn.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=label_encoder.classes_,
        yticklabels=label_encoder.classes_,
        ax=axs[1],
    )
    axs[1].set_title("Confusion Matrix")
    axs[1].set_ylabel("True Label")
    axs[1].set_xlabel("Predicted Label")

    pyplot.tight_layout()
    pyplot.savefig(f"plots/learner_plots.png")


if __name__ == "__main__":
    main()
