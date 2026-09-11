import os
from src.Analysis import generate_analysis, save_business_insights
from src.Analysis_Visualization import create_visualization
from src.Data_cleaning import clean_data, save_cleaned_data
from src.Data_Loader import load_data
from src.Data_transformation import transform_Data
from src.Report import create_report


def run_pipeline():
    chart_output_dir = "output/charts"
    report_output_path = "output/business_report.pdf"
    insights_output_path = "output/business_insights.txt"
    processed_data_path = "output/cleaned_engagement_data.csv"

    os.makedirs("output", exist_ok=True)
    os.makedirs(chart_output_dir, exist_ok=True)

    print("1. Loading raw data...")
    df = load_data()

    print("2. Cleaning data...")
    df_clean = clean_data(df)
    save_cleaned_data(df_clean, processed_data_path)

    print("3. Transforming data...")
    df_transformed = transform_Data(df_clean)

    print("4. Generating analysis...")
    analysis = generate_analysis(df_transformed)
    save_business_insights(analysis, insights_output_path)

    print("5. Creating visualizations...")
    create_visualization(df_transformed, chart_output_dir)

    print("6. Generating PDF report...")
    create_report(analysis, chart_output_dir, report_output_path)

    print("Pipeline finished successfully!")


if __name__ == "__main__":
    run_pipeline()