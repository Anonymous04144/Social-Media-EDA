pandas
numpy
matplotlib
seaborn
reportlab
openpyxl
pypdf


# Social Media Engagement EDA Project

A modular exploratory data analysis and reporting pipeline that cleans raw post metrics, calculates engagement KPIs, generates statistical charts, and compiles a comprehensive PDF business report.

## Project Structure
- `src/Data_Loader.py`: Ingestion logic with auto-fallback sample generation.
- `src/Data_Cleaning.py`: Deduplication, type conversion, and missing-value normalization.
- `src/Data_Transformation.py`: Engagement Rate calculations and timestamp decomposition.
- `src/Analysis.py`: Metric aggregations and insight text generation.
- `src/Analysis_Visualization.py`: Seaborn and Matplotlib visualization creation.
- `src/Report.py`: Automated multi-page PDF compilation using ReportLab.
- `main.py`: Pipeline execution orchestrator.

## Quickstart
1. Activate virtual environment:
   ```bash
   venv\Scripts\activate