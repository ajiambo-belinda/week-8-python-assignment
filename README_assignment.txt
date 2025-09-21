CORD-19 Assignment - How to run

1) Put metadata.csv in this folder (or upload in Streamlit).
2) Install dependencies:
   pip install -r requirements.txt

3) Run analysis script:
   python cord19_analysis.py --input metadata.csv --outdir outputs
   - Check outputs/ for images and CSVs.

4) Run Streamlit app:
   streamlit run streamlit_app.py
   - In the browser you can upload metadata.csv or it will read metadata.csv in the folder.

