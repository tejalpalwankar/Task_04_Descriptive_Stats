#!/usr/bin/env python3
"""
Polars Descriptive Statistics
Research Task 4: Facebook Posts Dataset
"""

import sys
import polars as pl

def load_data(filepath: str) -> pl.DataFrame:
    print(f"→ Loading data from {filepath} …")
    try:
        df = pl.read_csv(filepath)
    except Exception as e:
        print(f"‼Failed to read CSV: {e}")
        sys.exit(1)
    df = df.rename({c: c.strip() for c in df.columns})
    print(f"Loaded: {df.height} rows × {len(df.columns)} columns")
    return df

def analyze_dataset(df: pl.DataFrame) -> None:
    print("\n POLARS DATASET ANALYSIS")
    print("=" * 50)
    print(f"Rows: {df.height}, Columns: {len(df.columns)}")

    for col in df.columns:
        total = df.height

        # Count non-null appropriately
        if df[col].dtype.is_numeric():
            non_null = df[col].drop_nulls().len()
        else:
            non_null = df.filter(
                (pl.col(col).is_not_null()) & (pl.col(col) != "")
            ).height

        null = total - non_null

        print(f"\n--- {col} ---")
        print(f"Total: {total} | Non-null: {non_null} | Null: {null}")

        if df[col].dtype.is_numeric():
            m = df[col].mean()
            mi = df[col].min()
            ma = df[col].max()
            sd = df[col].std()
            print(f"Mean: {m:.2f} | Min: {mi} | Max: {ma} | Std: {sd:.2f}")
        else:
            unique = df[col].n_unique()
            vc = (
                df
                .filter(pl.col(col) != "")
                .group_by(col)
                .agg(pl.len().alias("count"))
                .sort("count", descending=True)
                .head(5)
            )
            print(f"Unique values: {unique}")
            print("Top 5 frequent values:")
            for val, cnt in vc.rows():
                print(f"  {val}: {cnt}")

def group_by_analysis(df: pl.DataFrame, group_cols: list) -> None:
    print(f"\n GROUP-BY ANALYSIS by {group_cols}")
    missing = [c for c in group_cols if c not in df.columns]
    if missing:
        print(f" Missing columns: {missing}")
        return

    stats = (
        df
        .group_by(group_cols)
        .agg([
            pl.col("Likes").mean().alias("Likes_mean"),
            pl.col("Likes").len().alias("Likes_count"),
            pl.col("Comments").mean().alias("Comments_mean"),
            pl.col("Comments").len().alias("Comments_count"),
            pl.col("Shares").mean().alias("Shares_mean"),
            pl.col("Shares").len().alias("Shares_count"),
        ])
    )

    print(f"Found {stats.height} groups")
    for row in stats.head(3).rows():
        key_vals = row[:len(group_cols)]
        metrics  = row[len(group_cols):]
        print(f"\nGroup: {dict(zip(group_cols, key_vals))} (count={metrics[1]})")
        print(f"  Likes: mean={metrics[0]:.2f}, count={metrics[1]}")
        print(f"  Comments: mean={metrics[2]:.2f}, count={metrics[3]}")
        print(f"  Shares: mean={metrics[4]:.2f}, count={metrics[5]}")

def main():
    print(" Starting Polars stats script")
    df = load_data("data/2024_fb_posts_president_scored_anon.csv")
    analyze_dataset(df)
    group_by_analysis(df, ["Facebook_Id"])
    group_by_analysis(df, ["Page Category"])
    group_by_analysis(df, ["Facebook_Id", "Page Category"])
    print("\nPolars analysis complete")

if __name__ == "__main__":
    main()
