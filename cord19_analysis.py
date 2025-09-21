"""
CORD-19 Metadata Analysis
Performs: Part 1-3 of your assignment:
 - Loads metadata.csv (CORD-19)
 - Explores and cleans the data
 - Produces basic analyses and saves plots to the `outputs/` folder

Usage:
    python cord19_analysis.py --input metadata.csv --outdir ./outputs

If metadata.csv is missing, a small sample file will be created (demo).
"""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

sns.set(style="whitegrid")

def load_data(path):
    path = Path(path)
    if not path.exists():
        print(f"[WARN] {path} not found. Creating a small sample dataframe for demo purposes.")
        sample = pd.DataFrame({
            "cord_uid": ["1","2","3","4"],
            "sha": ["a","b","c","d"],
            "source_x": ["bioRxiv","medRxiv","PMC","bioRxiv"],
            "title": ["COVID-19 and healthcare","Vaccine trial results","SARS-CoV-2 genomic analysis","Clinical outcomes study"],
            "doi": ["10.1","10.2",None,"10.4"],
            "pmcid": [None,"PMC1","PMC2",None],
            "pubmed_id": [None,"1001","1002",None],
            "license": ["cc-by","cc-by-nc","cc-by","cc-by"],
            "abstract": ["Study of COVID impacts","Vaccine was tested","Genome sequences collected","Patient outcomes analyzed"],
            "publish_time": ["2020-03-15","2021-06-01","2020-12-10","2021-01-20"],
            "journal": ["Journal A","Journal B","Journal C","Journal A"]
        })
        sample.to_csv(path, index=False)
        return sample
    df = pd.read_csv(path, low_memory=False)
    return df

def basic_exploration(df):
    print("Shape:", df.shape)
    print("\nColumns and dtypes:\n", df.dtypes)
    print("\nMissing value counts (top columns):\n", df.isna().sum().sort_values(ascending=False).head(20))
   

    print("\nNo numeric columns to describe.")

    print("\nSample rows:\n", df.head())

def clean_data(df):
    df = df.copy()
    # Trim column names
    df.columns = [c.strip() for c in df.columns]
    # Convert publish_time to datetime
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
        df["publish_year"] = df["publish_time"].dt.year
    else:
        df["publish_time"] = pd.NaT
        df["publish_year"] = pd.NA
    # Create abstract_word_count
    if "abstract" in df.columns:
        df["abstract"] = df["abstract"].fillna("")
        df["abstract_word_count"] = df["abstract"].apply(lambda s: len(str(s).split()))
    else:
        df["abstract_word_count"] = 0
    # Trim whitespace in string columns
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].str.strip()
    return df

def top_papers_by_year(df, outdir):
    counts = df["publish_year"].value_counts().sort_index()
    plt.figure(figsize=(8,4))
    counts.plot(kind="line", marker="o")
    plt.title("Number of papers by year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.tight_layout()
    outdir.mkdir(parents=True, exist_ok=True)
    plt.savefig(outdir / "papers_by_year.png")
    plt.close()
    print("[SAVED] papers_by_year.png")

def top_journals_bar(df, outdir, topn=10):
    if "journal" in df.columns:
        top = df["journal"].fillna("Unknown").value_counts().head(topn)
        plt.figure(figsize=(10,5))
        sns.barplot(x=top.values, y=top.index)
        plt.title(f"Top {topn} journals")
        plt.xlabel("Number of papers")
        plt.tight_layout()
        plt.savefig(outdir / "top_journals.png")
        plt.close()
        print("[SAVED] top_journals.png")
    else:
        print("[WARN] 'journal' column missing; skipping top journals plot.")

def words_in_titles(df, topn=30, outdir=Path("./outputs")):
    titles = df["title"].fillna("").astype(str).str.lower().tolist()
    words = []
    for t in titles:
        t_clean = re.sub(r'[^a-z0-9\\s]', ' ', t)
        words.extend([w for w in t_clean.split() if len(w) > 2])
    counter = Counter(words)
    most = counter.most_common(topn)
    outdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(most, columns=["word","count"]).to_csv(outdir / "top_title_words.csv", index=False)
    print("[SAVED] top_title_words.csv")
    return most

def main(args):
    df = load_data(args.input)
    print("=== BASIC EXPLORATION ===")
    basic_exploration(df)
    print("\n=== CLEANING ===")
    df_clean = clean_data(df)
    print("After cleaning - shape:", df_clean.shape)
    outdir = Path(args.outdir)
    print("\n=== PLOTS ===")
    top_papers_by_year(df_clean, outdir)
    top_journals_bar(df_clean, outdir)
    words = words_in_titles(df_clean, outdir=outdir)
    print("\nTop title words:\n", words[:20])
    df_clean.head(200).to_csv(outdir / "cleaned_sample.csv", index=False)
    print(f"\nSaved cleaned sample to {outdir / 'cleaned_sample.csv'}")
    print("\nDone. Check the outputs folder for images and CSVs.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="metadata.csv", help="Path to metadata.csv")
    parser.add_argument("--outdir", type=str, default="./outputs", help="Output directory for plots/csvs")
    args = parser.parse_args()
    main(args)
