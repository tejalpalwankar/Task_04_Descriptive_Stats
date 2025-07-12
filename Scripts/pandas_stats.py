#!/usr/bin/env python3
"""
Pandas Descriptive Statistics
Research Task 4: Facebook Posts Dataset
"""

import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV with pandas, strip whitespace from column names and string values.
    """
    df = pd.read_csv(filepath, encoding='utf-8')
    # Strip whitespace from headers
    df.columns = df.columns.str.strip()
    # Strip whitespace from object (string) columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
    return df

def analyze_dataset(df: pd.DataFrame) -> None:
    """
    Print overall dataset shape and per-column descriptive statistics.
    """
    print("\nPANDAS DATASET ANALYSIS")
    print("=" * 50)
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    for col in df.columns:
        series = df[col]
        total = len(series)
        non_null = series.count()
        null = total - non_null
        print(f"\n--- {col} ---")
        print(f"Total: {total} | Non-null: {non_null} | Null: {null}")
        
        if pd.api.types.is_numeric_dtype(series):
            mean = series.mean()
            mn = series.min()
            mx = series.max()
            std = series.std()
            print(f"Mean: {mean:.2f} | Min: {mn} | Max: {mx} | Std: {std:.2f}")
        else:
            clean = series.replace('', pd.NA).dropna()
            unique = clean.nunique()
            top5 = clean.value_counts().head(5)

            print(f"Unique values: {unique}")
            print("Top 5 frequent values:")
            for val, cnt in top5.items():
                print(f"  {val}: {cnt}")

def group_by_analysis(df: pd.DataFrame, group_cols: list) -> None:
    """
    Perform grouped analysis for numeric engagement metrics on specified group columns.
    """
    existing = [c for c in group_cols if c in df.columns]
    missing = set(group_cols) - set(existing)
    if missing:
        print(f"\n Missing columns for grouping: {missing}")
        return

    grouped = df.groupby(existing)
    print(f"\n GROUP-BY ANALYSIS by {existing} → {len(grouped)} groups")

    for i, (name, group) in enumerate(grouped):
        if i >= 3:  # show only first 3 groups
            break
        print(f"\nGroup {i+1}: {dict(zip(existing, name))} ({len(group)} rows)")
        for metric in ['Likes', 'Comments', 'Shares']:
            if metric in group.columns and pd.api.types.is_numeric_dtype(group[metric]):
                m = group[metric].mean()
                cnt = group[metric].count()
                print(f"  {metric}: mean={m:.2f}, count={cnt}")

def main():
    filepath = "data/2024_fb_posts_president_scored_anon.csv"
    df = load_data(filepath)
    analyze_dataset(df)
    group_by_analysis(df, ['Facebook_Id'])
    group_by_analysis(df, ['Page Category'])
    group_by_analysis(df, ['Facebook_Id', 'Page Category'])

if __name__ == "__main__":
    main()