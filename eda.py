import pandas as pd
import numpy as np

# -------------------------------------------------------------
# 1. Load Dataset
# -------------------------------------------------------------
csv_path = "Data/social_media_data.csv"
df = pd.read_csv(csv_path)

print("=" * 70)
print("1. DATASET OVERVIEW & SHAPE")
print(f"Total Rows: {df.shape[0]:,}, Total Columns: {df.shape[1]}")
print("=" * 70)

# -------------------------------------------------------------
# 2. Explore Dataset (Structure & Types)
# -------------------------------------------------------------
print("\n--- Summary Info ---")
print(df.info())

print("\n--- First 3 Records ---")
print(df.head(3).T)  # Transposed for easier reading in terminal

# -------------------------------------------------------------
# 3. Handle Missing Values
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("2. MISSING VALUE ASSESSMENT & HANDLING")
print("=" * 70)
missing_counts = df.isnull().sum()
print("Missing values per column:")
print(missing_counts[missing_counts > 0] if missing_counts.sum() > 0 else "No missing values found.")

# Fill or drop according to column data types
numeric_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(include=['object']).columns

# Fill numeric NaNs with median, text NaNs with 'Unknown'
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
df[categorical_cols] = df[categorical_cols].fillna("Unknown")

# -------------------------------------------------------------
# 4. Remove Duplicate Records
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("3. DUPLICATE RECORD REMOVAL")
print("=" * 70)
initial_rows = len(df)
df = df.drop_duplicates(subset=['post_id'])
duplicates_removed = initial_rows - len(df)
print(f"Duplicate rows removed: {duplicates_removed}")
print(f"Cleaned dataset rows: {len(df):,}")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['post_month'] = df['timestamp'].dt.to_period('M')

# Calculate total interaction metrics
df['total_engagement'] = df['likes_count'] + df['comments_count'] + df['shares_count']

# -------------------------------------------------------------
# 5. Analyze Likes and Comments
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("4. LIKES & COMMENTS SUMMARY STATISTICS")
print("=" * 70)
likes_comments_summary = df[['likes_count', 'comments_count', 'shares_count', 'total_engagement']].describe().T
print(likes_comments_summary[['mean', 'std', '50%', 'min', 'max']])

# -------------------------------------------------------------
# 6. Analyze Impressions & Engagement Rate
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("5. IMPRESSIONS & ENGAGEMENT DISTRIBUTION")
print("=" * 70)
impressions_summary = df[['impressions', 'engagement_rate']].describe().T
print(impressions_summary[['mean', 'std', '50%', 'min', 'max']])

# Correlation between impressions and engagement
corr_coeff = df['impressions'].corr(df['total_engagement'])
print(f"\nPearson correlation (Impressions vs Total Engagement): {corr_coeff:.4f}")

# -------------------------------------------------------------
# 7. Analyze Posting Trends (Monthly & Day of Week)
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("6. POSTING TRENDS")
print("=" * 70)
monthly_trend = df.groupby('post_month').agg(
    post_count=('post_id', 'count'),
    avg_engagement=('total_engagement', 'mean'),
    avg_impressions=('impressions', 'mean')
).reset_index()
print("Monthly Trend:")
print(monthly_trend.head(6))

dow_trend = df.groupby('day_of_week').agg(
    post_count=('post_id', 'count'),
    avg_engagement=('total_engagement', 'mean')
).sort_values(by='avg_engagement', ascending=False)
print("\nPerformance by Day of Week:")
print(dow_trend)

# -------------------------------------------------------------
# 8. Analyze Platform Performance
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("7. PLATFORM PERFORMANCE")
print("=" * 70)
platform_summary = df.groupby('platform').agg(
    total_posts=('post_id', 'count'),
    total_impressions=('impressions', 'sum'),
    avg_likes=('likes_count', 'mean'),
    avg_comments=('comments_count', 'mean'),
    avg_shares=('shares_count', 'mean'),
    avg_engagement=('total_engagement', 'mean'),
    mean_engagement_rate=('engagement_rate', 'mean')
).sort_values(by='avg_engagement', ascending=False)
print(platform_summary)

# -------------------------------------------------------------
# 9. Analyze User Engagement Growth & Buzz Change Rate
# -------------------------------------------------------------
print("\n" + "=" * 70)
print("8. USER GROWTH & BUZZ DYNAMICS")
print("=" * 70)
growth_cols = ['user_engagement_growth', 'buzz_change_rate']
print(df[growth_cols].describe().T[['mean', 'std', '50%', 'min', 'max']])

# -------------------------------------------------------------
# 10. Generate Business Insights
# -------------------------------------------------------------
top_platform = platform_summary.index[0]
best_day = dow_trend.index[0]
avg_post_eng = df['total_engagement'].mean()

print("\n" + "=" * 70)
print("9. AUTOMATED BUSINESS INSIGHTS")
print("=" * 70)
print(f"• Top Performing Platform: '{top_platform}' leads with an average of "
      f"{platform_summary.loc[top_platform, 'avg_engagement']:.1f} engagements per post.")
print(f"• Prime Posting Window: '{best_day}' yields the highest average interaction rate.")
print(f"• Content Volume vs Reach: Overall average engagement per post stands at {avg_post_eng:.1f}.")
if corr_coeff > 0.6:
    print("• Reach Efficiency: High direct correlation between impressions and total engagement.")
else:
    print("• Reach Efficiency: Low to moderate correlation between impressions and interactions; higher impression counts do not guarantee organic engagement.")

# Save cleaned data to output directory
output_cleaned_path = "output/cleaned_social_media_data.csv"
import os
os.makedirs("output", exist_ok=True)
df.to_csv(output_cleaned_path, index=False)
print(f"\n Cleaned dataset saved to: {output_cleaned_path}")