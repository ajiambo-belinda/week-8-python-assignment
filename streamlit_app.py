"""
Streamlit app for CORD-19 metadata exploration (Part 4)
Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(layout="wide", page_title="CORD-19 Data Explorer")

def load_data(path):
    path = Path(path)
    if not path.exists():
        st.warning(f"{path} not found. Place metadata.csv in the app folder or upload via sidebar.")
        return pd.DataFrame()
    return pd.read_csv(path, low_memory=False)

def main():
    st.title("CORD-19 Data Explorer")
    st.write("Simple exploration of COVID-19 research papers (metadata.csv)")

    # Allow upload
    data_file = st.sidebar.file_uploader("Upload metadata.csv", type=["csv"])
    if data_file is not None:
        df = pd.read_csv(data_file, low_memory=False)
    else:
        df = load_data("metadata.csv")

    if df.empty:
        st.info("No data loaded. Upload metadata.csv or place it in this folder as metadata.csv.")
        return

    # Basic cleaning
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
        df["publish_year"] = df["publish_time"].dt.year
    else:
        df["publish_year"] = None

    st.sidebar.header("Filters")
    min_year = int(df["publish_year"].dropna().min()) if df["publish_year"].dropna().any() else 2019
    max_year = int(df["publish_year"].dropna().max()) if df["publish_year"].dropna().any() else 2025
    year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))

    # Filter
    df_filtered = df[(df["publish_year"].notna()) & (df["publish_year"] >= year_range[0]) & (df["publish_year"] <= year_range[1])]

    st.subheader("Data sample (first 200 rows)")
    st.dataframe(df_filtered.head(200))

    st.subheader("Publications over time")
    counts = df_filtered["publish_year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8,3))
    counts.plot(ax=ax, marker='o')
    ax.set_xlabel("Year"); ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Top journals")
    if "journal" in df_filtered.columns:
        top = df_filtered["journal"].fillna("Unknown").value_counts().head(15)
        fig2, ax2 = plt.subplots(figsize=(8,4))
        sns.barplot(x=top.values, y=top.index, ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("No 'journal' column available.")

    st.subheader("Top words in titles (simple)")
    titles = df_filtered["title"].fillna("").astype(str).str.lower().tolist()
    from collections import Counter
    import re
    words = []
    for t in titles:
        t_clean = re.sub(r'[^a-z0-9\\s]', ' ', t)
        words.extend([w for w in t_clean.split() if len(w) > 2])
    top_words = Counter(words).most_common(30)
    st.table(pd.DataFrame(top_words, columns=["word","count"]))

    st.sidebar.markdown("### Export cleaned sample")
    if st.sidebar.button("Save cleaned sample to outputs/cleaned_sample.csv"):
        outdir = Path("outputs"); outdir.mkdir(exist_ok=True)
        df_filtered.head(200).to_csv(outdir / "cleaned_sample.csv", index=False)
        st.success("Saved to outputs/cleaned_sample.csv")

if __name__ == '__main__':
    main()
