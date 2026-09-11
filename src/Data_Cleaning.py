import pandas as pd

def clean_data(df):
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.drop_duplicates(subset=["post_id"])
    cleaned_df["post_date"] = pd.to_datetime(cleaned_df["post_date"], errors="coerce")
    cleaned_df = cleaned_df.dropna(subset=["post_date"])
    cleaned_df["platform"] = cleaned_df["platform"].astype(str).str.strip().str.title()
    cleaned_df["content_type"] = cleaned_df["content_type"].astype(str).str.strip().str.title()
    
    num_cols = ["impressions", "reach", "likes", "comments", "shares", "saves"]
    for col in num_cols:
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce").fillna(0)
        
    return cleaned_df

def save_cleaned_data(df, output_path):
    df.to_csv(output_path, index=False)
