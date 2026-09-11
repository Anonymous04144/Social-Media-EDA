import pandas as pd

def generate_analysis(df):
    analysis_results = {}
    analysis_results["platform_summary"] = df.groupby("platform").agg(
        total_posts=("post_id", "count"),
        avg_impressions=("impressions", "mean"),
        avg_engagements=("total_engagements", "mean"),
        avg_engagement_rate=("engagement_rate", "mean")
    ).round(2).to_dict(orient="index")
    
    analysis_results["content_summary"] = df.groupby("content_type").agg(
        total_posts=("post_id", "count"),
        avg_engagement_rate=("engagement_rate", "mean"),
        total_shares=("shares", "sum")
    ).round(2).to_dict(orient="index")
    
    analysis_results["overall"] = {
        "total_posts": int(len(df)),
        "avg_engagement_rate": round(float(df["engagement_rate"].mean()), 2),
        "top_performing_platform": df.groupby("platform")["engagement_rate"].mean().idxmax(),
        "top_performing_content": df.groupby("content_type")["engagement_rate"].mean().idxmax()
    }
    return analysis_results

def save_business_insights(analysis, output_path):
    with open(output_path, "w") as f:
        f.write("=== SOCIAL MEDIA ENGAGEMENT BUSINESS INSIGHTS ===\n\n")
        f.write(f"Total Posts Analyzed: {analysis['overall']['total_posts']}\n")
        f.write(f"Average Global Engagement Rate: {analysis['overall']['avg_engagement_rate']}%\n")
        f.write(f"Top Performing Platform: {analysis['overall']['top_performing_platform']}\n")
        f.write(f"Top Performing Content Type: {analysis['overall']['top_performing_content']}\n\n")
