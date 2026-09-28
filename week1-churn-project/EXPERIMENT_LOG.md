# Experiment Log

One entry per run. Data version v1 is the original Kaggle file, checked by its SHA-256 fingerprint:
`2350c86e2564a1401e10106ac4121eec23a884d6f53fffeeba8a9e950b3c86a4`

Settings shared by all runs: stratified 80/20 train and test split, random_state 42, test set of 23,128 rows (12.19% churn). Excluded columns: Churn Reason (leakage) and sensitive attributes (gender, marital status, income, education, occupation, address).

| Date | Data Version | Settings | Result | Takeaway |
|---|---|---|---|---|
| 2026-09-28 | v1 | Majority-class baseline (DummyClassifier, most_frequent). Features: Balance, NumComplaints, NumOfProducts, Credit Score | Accuracy 0.88, churn recall 0.00, churn precision 0.00, ROC-AUC 0.50 | Looks accurate but never finds a churner. Confirms accuracy is the wrong metric here. |
| 2026-09-28 | v1 | Logistic regression (StandardScaler, max_iter 1000), same four features, threshold 0.5 | Churn precision 1.00, churn recall 1.00, ROC-AUC 1.00 | Far too good to be real. Investigated before trusting it. |
| 2026-09-28 | v1 | Same logistic regression, threshold lowered to 0.15 | Recall 1.00, precision 0.90 | Lowering the threshold only costs precision, since recall is already at the ceiling. |
| 2026-09-28 | v1 | Same logistic regression, 5-fold cross-validation (ROC-AUC) | 1.00 in all five folds | Not a lucky split. The result is stable. |
| 2026-09-28 | v1 | Diagnostic: single features and feature pairs, logistic regression, test set ROC-AUC | Balance alone 0.94. Other single features 0.66 to 0.69. Balance with one other feature 0.96 to 0.97. Pairs without Balance 0.72 to 0.74. | No single feature explains it, but the four together separate the classes perfectly. The label was most likely generated from a rule built on these features, so the data is synthetic and the score says little about a real bank. |

## Decisions recorded

- Churn Reason is excluded from every run because it reveals the target.
- The original recall target of 60 to 70% was dropped because the baseline already reaches about 100% on this dataset.
- Next step: repeat the comparison on real bank data before drawing any conclusion about model value.
