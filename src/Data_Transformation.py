import pandas as pd

def transform_Data(df):
    transformed_df = df.copy()
    
    # Interaction aggregates
    transformed_df["total_engagements"] = (
        transformed_df["likes"] + 
        transformed_df["comments"] + 
        transformed_df["shares"] + 
        transformed_df["saves"]
    )
    
    # Engagement Rate (%) based on impressions
    transformed_df["engagement_rate"] = (
        (transformed_df["total_engagements"] / transformed_df["impressions"].replace(0, 1)) * 100
    ).round(2)
    
    # Date/Time breakdown
    transformed_df["day_name"] = transformed_df["post_date"].dt.day_name()
    transformed_df["post_hour"] = transformed_df["post_date"].dt.hour
    
    return transformed_df