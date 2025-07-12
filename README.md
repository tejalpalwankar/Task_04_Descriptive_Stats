# Task_04_Descriptive_Stats

## 📄 Overview
This project performs descriptive statistical analysis on the `2024_fb_posts_president_scored_anon.csv` dataset using three different approaches:

- ✅ Pure Python (`scripts/pure_python_stats.py`)
- 🐼 Pandas (`scripts/pandas_stats.py`)
- ⚡ Polars (`scripts/polars_stats.py`)

The goal is to extract insights, handle messy or incomplete data, and compare performance across different processing tools.

---

## 📁 Dataset
Place the dataset `2024_fb_posts_president_scored_anon.csv` inside the `data/` directory:

```
project_root/
│
├── data/
│   └── 2024_fb_posts_president_scored_anon.csv
│
├── scripts/
│   ├── pure_python_stats.py
│   ├── pandas_stats.py
│   └── polars_stats.py
```

Ensure your `.gitignore` includes:
```
data/
__pycache__/
*.pyc
```

---

## ⚙️ Setup

### ✅ Step 1: Install dependencies

```bash
pip install pandas polars
```

### ✅ Step 2: Run scripts

```bash
# Run Pure Python script
python3 scripts/pure_python_stats.py

# Run Pandas script
python3 scripts/pandas_stats.py

# Run Polars script
python3 scripts/polars_stats.py
```

---

## 📊 What Each Script Does

Each script prints:

- Total rows and columns in the dataset
- Count of non-null and null values per column
- For numeric columns: Mean, Min, Max, Standard Deviation
- For categorical columns: Unique values, Top 5 frequent values
- Group-wise summaries:
  - Interactions per `Facebook_Id`
  - Interactions by `Page Category`
  - Interactions by `(Facebook_Id, Page Category)` pair

---

## 🔍 Key Insights

### 🟡 General Dataset Stats
- Total Posts: **19,009**
- Columns: **56**

### 🔹 High Engagement Observed
- Average Likes: ~2,378
- Average Shares: ~321
- Average Comments: ~902

### 🔹 Disproportionate Visibility
- A small number of `Facebook_Id`s contributed **more than 70%** of all interactions.
- Example: Top user received **~39,000 average likes** per post.

### 🔹 By Page Category
| Category              | Avg Likes | Avg Shares | Avg Comments |
|-----------------------|-----------|------------|--------------|
| POLITICAL_CANDIDATE   | ~11,402   | 1305       | 4422         |
| POLITICIAN            | ~1,715    | 303        | 571          |
| PERSON                | ~404      | 76         | 155          |
| ACTOR                 | ~256      | 53         | 86           |

---

## 💡 Learning Outcomes

- Deepened understanding of basic and advanced data wrangling using Python
- Explored multiple libraries (`Pandas`, `Polars`, `Pure Python`) and their performance tradeoffs
- Hands-on practice in:
  - Handling missing/null values
  - GroupBy operations
  - Text cleanup (e.g., stripping whitespace)
  - Extracting top frequent categories
- Gained insight into political content distribution and engagement trends on Facebook

---

## 🧪 Tested On

- Python 3.10+
- Pandas 2.x
- Polars 0.20+
- macOS and Unix-compatible systems

---

## 📌 Notes

- Polars is significantly faster than Pandas for larger datasets.
- Pure Python is educational but not ideal for real-world data science tasks.
- Missing values in columns like `Page Admin Top Country` and `Page Category` should be handled explicitly in production use cases.

---
