import os
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualization(df, chart_dir):
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="platform", y="engagement_rate", estimator="mean", errorbar=None, palette="mako")
    plt.title("Average Engagement Rate (%) by Platform")
    plt.tight_layout()
    plt.savefig(os.path.join(chart_dir, "platform_engagement.png"), dpi=300)
    plt.close()
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="content_type", y="total_engagements", palette="Set2", showfliers=False)
    plt.title("Total Engagements by Content Type")
    plt.tight_layout()
    plt.savefig(os.path.join(chart_dir, "content_engagements.png"), dpi=300)
    plt.close()
    
    plt.figure(figsize=(7, 6))
    metric_cols = ["impressions", "reach", "likes", "comments", "shares", "saves", "engagement_rate"]
    sns.heatmap(df[metric_cols].corr(), annot=True, cmap="Blues", fmt=".2f")
    plt.title("Interaction Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(chart_dir, "correlation_heatmap.png"), dpi=300)
    plt.close()
