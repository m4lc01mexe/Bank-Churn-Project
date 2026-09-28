# Bank Customer Churn: Week 1 Tutorial (AI Solution Design, CRISP-DM and Responsible Problem Framing)

**Author:** Amogelang Maforaga (Student ID: Fbda23-021)
**Course:** BSc Business Intelligence and Data Analytics, Botswana Accountancy College

## 1. What this project is

This project frames and audits a customer churn problem for a retail bank, with Botswana as the intended application. Churn means a customer closes their account or leaves the bank. The aim is to decide whether a machine learning model is appropriate, to check the data honestly, and to set a baseline that any later model must beat.

| Task | What it covers | Where it lives |
|---|---|---|
| Task 1 | Project charter | `docs/Week1_Task1_and_Task4.docx` |
| Task 2 | Dataset audit | `notebooks/Week1_Task2_and_Task3.ipynb` |
| Task 3 | Exploratory analysis and baseline models | `notebooks/Week1_Task2_and_Task3.ipynb` |
| Task 4 | Checkpoint: is AI the right approach here? | `docs/Week1_Task1_and_Task4.docx` |

## 2. Important limitation, read this first

The dataset comes from Kaggle and appears to be **synthetic**. Names and addresses are US-formatted, demographic splits are almost perfectly even, and a simple logistic regression scores about 100% on it. So this project demonstrates the method, and its scores say very little about how a model would perform at a real Botswana bank.

## 3. Folder layout

```
week1-churn-project/
    README.md                     <- this file
    EXPERIMENT_LOG.md             <- one entry per run: settings, data version, result, takeaway
    requirements.txt              <- library versions used
    .gitignore
    data/
        raw/                      <- original Kaggle CSV goes here. Never edited or overwritten.
        processed/                <- files created by the notebook (recreated on every run)
    notebooks/
        Week1_Task2_and_Task3.ipynb   <- exploration and analysis
    src/
        churn_utils.py            <- reusable code: paths, feature list, split, threshold table
    docs/
        Week1_Task1_and_Task4.docx    <- written charter and checkpoint
```

Why it is organised this way: raw data is kept apart from processed data so the original can always be recovered. The notebook is for exploration, and anything reused lives in `src/` so settings such as the random seed are defined once.

## 4. Getting the data

1. Download the Kaggle bank churn dataset: https://www.kaggle.com/datasets/navneetmuliya/bank-churn-dataset
2. Save the file as `data/raw/bank_churn_data.csv` (exact name, exact folder).
3. Optional check that you have the same file used in this project (data version v1). The notebook also does this automatically in its first cell.

   Windows (Command Prompt, from the project folder):
   ```
   certutil -hashfile data\raw\bank_churn_data.csv SHA256
   ```
   The result should be:
   ```
   2350c86e2564a1401e10106ac4121eec23a884d6f53fffeeba8a9e950b3c86a4
   ```
   The file should have 115,640 rows and 22 columns and be about 21 MB.

## 5. Setup from scratch (Windows, VS Code)

No earlier experience is assumed.

### Step 1: Install Python
1. Download Python 3.9 or newer from https://www.python.org/downloads/
2. Run the installer and **tick "Add Python to PATH"** before clicking Install.
3. In a new Command Prompt, check it worked:
   ```
   python --version
   ```

### Step 2: Install VS Code and its extensions
1. Download VS Code from https://code.visualstudio.com/
2. Install two extensions from the Extensions panel: **Python** and **Jupyter** (both by Microsoft).

### Step 3: Open the project folder
In VS Code choose **File, then Open Folder**, and select the project folder (the one containing this README).

### Step 4: Install the libraries
Open the VS Code terminal (**Terminal, then New Terminal**) and run:
```
python -m pip install -r requirements.txt
```
If a pinned version cannot be installed on your Python, run `python -m pip install pandas numpy matplotlib scikit-learn ipykernel` instead.

### Step 5: Open the notebook and choose the kernel
1. Open `notebooks/Week1_Task2_and_Task3.ipynb`.
2. Click **Select Kernel** at the top right, choose **Python Environments**, and pick the Python where you ran Step 4.

### Step 6: Run it
Click **Run All**. It takes about a minute. The notebook finds the data by itself, so there is no path to edit. Run cells from top to bottom because later cells depend on earlier ones.

## 6. What you should see

| Check | Expected result |
|---|---|
| First cell output | `Raw data matches expected version (v1): True` |
| Data shape | 115,640 rows, 22 columns |
| Missing values and duplicate rows | 0 |
| Churn rate | about 12.2% (14,094 churned, 101,546 stayed) |
| Train and test churn rate | about 12.2% in both |
| Test set size | 23,128 rows |
| Majority-class baseline | about 88% accuracy, 0% churn recall, ROC-AUC 0.5 |
| Logistic regression | precision and recall about 1.00, ROC-AUC about 1.0 |
| 5-fold cross-validated ROC-AUC | about 1.0 in every fold |
| New file created | `data/processed/churn_model_ready.csv` |

The full record of runs is in `EXPERIMENT_LOG.md`.

## 7. Key findings in plain language

- **Class imbalance:** only about 12% of customers churn, so accuracy is misleading. Precision, recall, F1 and ROC-AUC on the churn class are used instead.
- **Leakage:** `Churn Reason` reveals the answer (it says "No Reason" for everyone who stayed), so it is excluded.
- **Sensitive attributes:** gender, marital status, income, education, occupation and address are kept out of the models.
- **Near-perfect baseline:** a simple logistic regression on Balance, NumComplaints, NumOfProducts and Credit Score separates churners almost perfectly. No single feature does this (Balance alone gives an AUC of about 0.94), so the label was probably generated from a rule built on these features. This is a warning sign about the data, not evidence of a great model.

## 8. Reproducibility notes

- **Data version:** v1, identified by the SHA-256 fingerprint in section 4.
- **Randomness:** the split is stratified 80/20 with `random_state=42`, set once in `src/churn_utils.py`, so results are identical on every run.
- **Libraries:** versions are listed in `requirements.txt` (Python 3.12, pandas 3.0.2, numpy 2.4.4, matplotlib 3.10.8, scikit-learn 1.8.0 were used).
- **Experiment log:** every reported result has an entry in `EXPERIMENT_LOG.md` with its settings and data version.
- **Version control:** see section 9.

## 9. Version control (git)

Install Git from https://git-scm.com/ if needed, then run these commands once in the project folder. Raw and processed data are ignored by `.gitignore` because the raw file is downloaded from Kaggle and the processed file is recreated by the notebook.

Set your identity (first time only):
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Start the repository and record the work in clear steps:
```
git init
git add README.md requirements.txt .gitignore data/raw/.gitkeep data/processed/.gitkeep
git commit -m "Set up project structure, README and requirements"

git add src/
git commit -m "Add reusable helpers for paths, features and train/test split"

git add notebooks/
git commit -m "Add Task 2 dataset audit and Task 3 exploratory analysis and baselines"
git tag -a v0.1-task2-task3 -m "Notebook version used for the Task 2 and Task 3 results"

git add EXPERIMENT_LOG.md
git commit -m "Record baseline experiments in the experiment log"

git add docs/
git commit -m "Add Task 1 charter and Task 4 checkpoint document"
git tag -a v1.0-week1-submission -m "Version submitted for Week 1"
```

Rules to keep following: one clear message per commit that says what changed and why, and a tag on the exact version behind each reported result. Check history at any time with `git log --oneline` and tags with `git tag`.

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `pip` is not recognised | Use `python -m pip install ...`. If `python` is also not recognised, reinstall Python and tick "Add Python to PATH". |
| `ModuleNotFoundError: No module named 'sklearn'` | Run Step 4, then check the kernel in Step 5 matches the Python you installed into. Restart the kernel. |
| `ModuleNotFoundError: No module named 'src'` | Open the project folder itself in VS Code (Step 3), not just the notebook file, so the notebook runs from `notebooks/`. |
| `FileNotFoundError` for the CSV | The file is not at `data/raw/bank_churn_data.csv`. Check the folder and the exact name. |
| First cell prints `False` for the data version | Your CSV differs from the one used here. Results may not match the tables above. |
| Yellow underlines on `sklearn` imports | VS Code is checking a different Python. Press `Ctrl+Shift+P`, run **Python: Select Interpreter**, and choose the right one. |
| Red errors such as "Incorrect syntax near '='" and "No connection selected" | The cells are set to **SQL**. Click the language label at the bottom right of each cell and switch to **Python**. |
| A cell fails with a name that is not defined | An earlier cell was skipped. Restart the kernel and use **Run All**. |

## 11. Data and ethics note

The dataset is synthetic and contains attributes that would be sensitive in real life (gender, marital status, income, address). Nothing in this project should be used to make real decisions about real customers. Before any real deployment, the approach would need to be retested on genuine local data, and the model checked for indirect discrimination through proxies such as address.
