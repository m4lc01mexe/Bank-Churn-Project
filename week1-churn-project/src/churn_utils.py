"""Reusable helpers for the bank churn project.

Keeping these in src/ means the notebook stays focused on exploration, and
the same settings (features, split, random seed) are used everywhere.
"""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

# Paths are built from the location of this file, so they work no matter
# which folder the notebook or script is run from.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "bank_churn_data.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "churn_model_ready.csv"

# Expected fingerprint of the original Kaggle file (data version v1).
RAW_SHA256 = "2350c86e2564a1401e10106ac4121eec23a884d6f53fffeeba8a9e950b3c86a4"

TARGET = "Churn Flag"
FEATURES = ["Balance", "NumComplaints", "NumOfProducts", "Credit Score"]

# Excluded from modelling. Churn Reason leaks the target; the rest are sensitive.
LEAKAGE_COLS = ["Churn Reason"]
SENSITIVE_COLS = ["Gender", "Marital Status", "Income", "Education Level",
                  "Occupation", "Address"]

TEST_SIZE = 0.2
RANDOM_STATE = 42


def load_data(path=RAW_PATH):
    """Read the raw CSV. The raw file is only ever read, never overwritten."""
    return pd.read_csv(path)


def split_data(X, y):
    """Stratified train/test split with the project's fixed settings."""
    return train_test_split(X, y, test_size=TEST_SIZE,
                            stratify=y, random_state=RANDOM_STATE)


def threshold_table(y_true, proba, thresholds=(0.5, 0.4, 0.3, 0.2, 0.15)):
    """Recall and precision for the churn class at several probability thresholds."""
    rows = []
    for t in thresholds:
        pred = (proba >= t).astype(int)
        tp = int(((pred == 1) & (y_true == 1)).sum())
        fp = int(((pred == 1) & (y_true == 0)).sum())
        fn = int(((pred == 0) & (y_true == 1)).sum())
        rows.append({
            "threshold": t,
            "recall": round(tp / (tp + fn), 3) if (tp + fn) else 0,
            "precision": round(tp / (tp + fp), 3) if (tp + fp) else 0,
        })
    return pd.DataFrame(rows)
