import sqlite3
import pandas as pd

# 1. Load CSV data
csv_path = "Data/social_media_data.csv"
df = pd.read_csv(csv_path)

# 2. Push to an in-memory SQLite database
conn = sqlite3.connect(":memory:")
df.to_sql("social_media_posts", conn, index=False, if_exists="replace")

print(" Dataset loaded into SQLite successfully!\n" + "=" * 60)

# -------------------------------------------------------------
# SQL Tasks Mapped to Your Dataset Columns
# -------------------------------------------------------------

queries = {
    "1. Total Posts": """
        SELECT COUNT(post_id) AS total_posts 
        FROM social_media_posts;
    """,
    "2. Average Likes per Post": """
        SELECT ROUND(AVG(likes_count), 2) AS avg_likes 
        FROM social_media_posts;
    """,
    "3. Top 10 Most Engaged Posts": """
        SELECT 
            post_id, 
            platform, 
            likes_count, 
            comments_count, 
            shares_count,
            (likes_count + comments_count + shares_count) AS total_engagement
        FROM social_media_posts
        ORDER BY total_engagement DESC
        LIMIT 10;
    """,
    "4. Engagement by Platform": """
        SELECT 
            platform,
            COUNT(post_id) AS total_posts,
            SUM(likes_count + comments_count + shares_count) AS platform_engagement,
            ROUND(AVG(likes_count + comments_count + shares_count), 2) AS avg_engagement_per_post,
            ROUND(AVG(likes_count), 2) AS avg_likes,
            ROUND(AVG(comments_count), 2) AS avg_comments
        FROM social_media_posts
        GROUP BY platform
        ORDER BY platform_engagement DESC;
    """,
    "5. Monthly Posting Trends": """
        SELECT 
            SUBSTR(timestamp, 1, 7) AS post_month,
            COUNT(post_id) AS total_posts,
            SUM(likes_count + comments_count + shares_count) AS monthly_engagement,
            SUM(impressions) AS total_impressions
        FROM social_media_posts
        GROUP BY post_month
        ORDER BY post_month ASC;
    """,
    "6. Average Comments per Post": """
        SELECT ROUND(AVG(comments_count), 2) AS avg_comments 
        FROM social_media_posts;
    """,
    "7. Top 10 Posts with Highest Impressions": """
        SELECT 
            post_id, 
            platform, 
            impressions, 
            (likes_count + comments_count + shares_count) AS total_engagement
        FROM social_media_posts
        ORDER BY impressions DESC
        LIMIT 10;
    """,
    "8. Rank Posts Based on Engagement": """
        SELECT 
            post_id,
            platform,
            (likes_count + comments_count + shares_count) AS total_engagement,
            DENSE_RANK() OVER (ORDER BY (likes_count + comments_count + shares_count) DESC) AS rank_overall
        FROM social_media_posts
        LIMIT 10;
    """,
    "9. Top Hashtags Usage": """
        SELECT 
            hashtags,
            COUNT(*) AS usage_count,
            ROUND(AVG(likes_count + comments_count + shares_count), 2) AS avg_engagement
        FROM social_media_posts
        WHERE hashtags IS NOT NULL AND hashtags != ''
        GROUP BY hashtags
        ORDER BY usage_count DESC
        LIMIT 10;
    """,
    "10. Engagement Rate Calculation": """
        SELECT 
            platform,
            SUM(likes_count + comments_count + shares_count) AS total_engagement,
            SUM(impressions) AS total_impressions,
            ROUND((CAST(SUM(likes_count + comments_count + shares_count) AS FLOAT) / NULLIF(SUM(impressions), 0)) * 100, 2) AS overall_engagement_rate_pct
        FROM social_media_posts
        GROUP BY platform
        ORDER BY overall_engagement_rate_pct DESC;
    """
}

# Execute and display each query
for title, sql in queries.items():
    print(f"\n--- {title} ---")
    result_df = pd.read_sql_query(sql, conn)
    print(result_df)

conn.close()