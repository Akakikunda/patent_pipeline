# Patent Data Pipeline

## GitHub Repository
https://github.com/Akakikunda/patent_pipeline

## Live Dashboard
https://patentpipeline-tzappuglgg48y4punnnvwr.streamlit.app

## Project Requirements Met
- SQL database with 4 tables (patents, inventors, companies, relationships)
- 7 SQL queries (JOIN, CTE, RANKING)
- Console report
- CSV reports (top_inventors.csv, top_companies.csv, country_trends.csv)
- JSON report (patent_report.json)
- Clean data files (clean_patents.csv, clean_inventors.csv, clean_companies.csv)
- schema.sql

## How to Run
```bash
pip install pandas streamlit plotly
python pipeline.py
streamlit run dashboard.py
```
