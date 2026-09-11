import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATA_PATH = "output/cleaned_social_media_data.csv" if os.path.exists("output/cleaned_social_media_data.csv") else "Data/social_media_data.csv"
CHARTS_DIR = "output/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Chart 9: Reach Distribution Histogram
plt.figure(figsize=(7, 4))
sns.histplot(df['impressions'], kde=True, bins=30, color='#7C3AED')
plt.title("Reach / Impressions Distribution", fontsize=12, fontweight='bold')
plt.xlabel("Impressions (Reach)")
plt.ylabel("Post Count")
plt.tight_layout()
reach_path = os.path.join(CHARTS_DIR, "9_reach_distribution.png")
plt.savefig(reach_path, dpi=200)
plt.close()
print(f"Saved: {reach_path}")

# Chart 10: Pair Plot
pair_cols = ['likes_count', 'comments_count', 'shares_count', 'impressions']
available_cols = [c for c in pair_cols if c in df.columns]

g = sns.pairplot(df[available_cols], diag_kind='kde', corner=False, plot_kws={'alpha': 0.5, 's': 20})
g.fig.subplots_adjust(top=0.93)
g.fig.suptitle("Engagement Metrics Pair Plot", fontsize=14, fontweight='bold')
pairplot_path = os.path.join(CHARTS_DIR, "10_pair_plot.png")
g.savefig(pairplot_path, dpi=200)
plt.close()
print(f"Saved: {pairplot_path}")
