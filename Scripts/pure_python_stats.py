#!/usr/bin/env python3
"""
Pure Python Descriptive Statistics
Research Task 4: Facebook Posts Dataset
"""

import csv
import math
import time
from collections import Counter, defaultdict
from typing import Dict, List, Any


class PythonStatsAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data: List[Dict[str, str]] = []
        self.headers: List[str] = []
        self.stats: Dict[str, Any] = {}

    def load_data(self) -> None:
        print("Loading data (comma-separated)...")
        start = time.time()

        with open(self.filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f, delimiter=',')
            # strip whitespace from headers
            self.headers = [h.strip() for h in reader.fieldnames]

            for row in reader:
                # strip whitespace from keys and values
                clean_row = {k.strip(): v.strip() for k, v in row.items()}
                self.data.append(clean_row)

        duration = time.time() - start
        print(f" Loaded {len(self.data)} rows, {len(self.headers)} columns in {duration:.2f}s")
        print(f"Sample columns: {self.headers[:5]}")

    def is_numeric(self, v: str) -> bool:
        try:
            float(v)
            return True
        except:
            return False

    def to_numeric(self, vals: List[str]) -> List[float]:
        return [float(x) for x in vals if self.is_numeric(x)]

    def mean(self, nums: List[float]) -> float:
        return sum(nums) / len(nums) if nums else 0

    def std(self, nums: List[float]) -> float:
        if len(nums) < 2:
            return 0
        m = self.mean(nums)
        return math.sqrt(sum((x - m) ** 2 for x in nums) / (len(nums) - 1))

    def analyze_column(self, col: str) -> Dict[str, Any]:
        # collect all values for column (including empty)
        vals = [row.get(col, "") for row in self.data]
        non_null = [v for v in vals if v != ""]
        stats: Dict[str, Any] = {
            "count": len(vals),
            "non_null": len(non_null),
            "null": len(vals) - len(non_null)
        }

        nums = self.to_numeric(non_null)
        if nums:
            stats.update({
                "type": "numeric",
                "mean": self.mean(nums),
                "min": min(nums),
                "max": max(nums),
                "std": self.std(nums)
            })
        else:
            freq = Counter(non_null)
            stats.update({
                "type": "categorical",
                "unique": len(freq),
                "top_5": freq.most_common(5)
            })

        return stats

    def analyze_dataset(self) -> None:
        print("\n OVERALL DATASET STATS")
        print("=" * 50)
        print(f"Rows: {len(self.data)}, Columns: {len(self.headers)}")
        for col in self.headers:
            st = self.analyze_column(col)
            print(f"\n--- {col} ({st['type']}) ---")
            print(f"Total: {st['count']} | Non-null: {st['non_null']} | Null: {st['null']}")
            if st["type"] == "numeric":
                print(f"Mean: {st['mean']:.2f} | Min: {st['min']} | Max: {st['max']} | Std: {st['std']:.2f}")
            else:
                print(f"Unique: {st['unique']} | Top 5: {st['top_5']}")

    def group_by(self, group_cols: List[str]) -> None:
        print(f"\nGROUP-BY STATS: {group_cols}")
        missing = [c for c in group_cols if c not in self.headers]
        if missing:
            print(f" Missing columns: {missing}")
            return

        groups = defaultdict(list)
        for row in self.data:
            key = tuple(row[c] for c in group_cols)
            groups[key].append(row)

        print(f"Found {len(groups)} groups")
        # show stats on first 3 groups
        for i, (key, rows) in enumerate(list(groups.items())[:3], 1):
            print(f"\nGroup {i}: {dict(zip(group_cols, key))} ({len(rows)} rows)")
            for col in ["Likes", "Comments", "Shares"]:
                if col in self.headers:
                    vals = [r[col] for r in rows if r[col] != ""]
                    nums = self.to_numeric(vals)
                    if nums:
                        print(f"  {col}: mean={self.mean(nums):.2f}, count={len(nums)}")

def main():
    analyzer = PythonStatsAnalyzer("data/2024_fb_posts_president_scored_anon.csv")
    try:
        analyzer.load_data()
        analyzer.analyze_dataset()
        # Group by real columns
        analyzer.group_by(["Facebook_Id"])
        analyzer.group_by(["Page Category"])
        analyzer.group_by(["Facebook_Id", "Page Category"])
    except FileNotFoundError:
        print(" data file not found: data/2024_fb_posts_president_scored_anon.csv")

if __name__ == "__main__":
    main()
