# CORD-19 Metadata Assignment - Short Report

## Tasks completed
- Part 1: Loaded metadata.csv; printed shape, dtypes, missing value counts, sample rows.
- Part 2: Converted publish_time to datetime, extracted publish_year, created abstract_word_count, trimmed whitespace.
- Part 3: Produced visualizations: papers_by_year, top_journals; saved top title words.
- Part 4: Built a Streamlit app for interactive exploration.
- Part 5: Documented steps, saved outputs and sample CSVs.

## Example findings (from sample run)
- Publication years (from sample) cluster around 2020–2021.
- Top words in titles include "covid", "vaccine", "study" (sample results).
- Challenges: metadata.csv can be very large; use sampling during development.

## Reflection
- Using pandas for exploratory data analysis (EDA) is efficient and concise.
- Streamlit allowed a quick interactive interface to share results.
