import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Configure visual style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 9, 'figure.autolayout': True})

# Define paths
DATA_PATH = "output/cleaned_social_media_data.csv" if os.path.exists("output/cleaned_social_media_data.csv") else "Data/social_media_data.csv"
CHARTS_DIR = "output/charts"
PDF_OUTPUT_PATH = "output/Social_Media_Engagement_Report.pdf"

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

# -------------------------------------------------------------------------
# 1. Load and Verify Data
# -------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

# Ensure numeric types and derived columns
numeric_cols = ['likes_count', 'comments_count', 'shares_count', 'impressions']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

if 'total_engagement' not in df.columns:
    df['total_engagement'] = df['likes_count'] + df['comments_count'] + df['shares_count']

if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['post_month'] = df['timestamp'].dt.to_period('M').astype(str)

# -------------------------------------------------------------------------
# 2. Generate Chart Suite
# -------------------------------------------------------------------------
print("Generating charts...")

chart_files = {}

# Chart 1: Likes Distribution
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(df['likes_count'], kde=True, bins=25, color='#2563EB', ax=ax)
ax.set_title("Likes Distribution Histogram", fontweight='bold')
ax.set_xlabel("Likes Count")
ax.set_ylabel("Frequency")
chart_files['likes_dist'] = os.path.join(CHARTS_DIR, "1_likes_distribution.png")
fig.savefig(chart_files['likes_dist'], dpi=200)
plt.close(fig)

# Chart 2: Comments Distribution
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(df['comments_count'], kde=True, bins=25, color='#059669', ax=ax)
ax.set_title("Comments Distribution Histogram", fontweight='bold')
ax.set_xlabel("Comments Count")
ax.set_ylabel("Frequency")
chart_files['comments_dist'] = os.path.join(CHARTS_DIR, "2_comments_distribution.png")
fig.savefig(chart_files['comments_dist'], dpi=200)
plt.close(fig)

# Chart 3: Platform Performance Bar Chart
fig, ax = plt.subplots(figsize=(6, 3.5))
platform_perf = df.groupby('platform')['total_engagement'].mean().sort_values(ascending=False)
sns.barplot(x=platform_perf.index, y=platform_perf.values, palette='Blues_r', ax=ax)
ax.set_title("Average Engagement by Platform", fontweight='bold')
ax.set_ylabel("Mean Engagement")
ax.set_xlabel("Platform")
chart_files['platform_bar'] = os.path.join(CHARTS_DIR, "3_platform_bar.png")
fig.savefig(chart_files['platform_bar'], dpi=200)
plt.close(fig)

# Chart 4: Engagement Share by Platform (Pie)
fig, ax = plt.subplots(figsize=(6, 3.5))
platform_share = df.groupby('platform')['total_engagement'].sum()
ax.pie(platform_share, labels=platform_share.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
ax.set_title("Total Engagement Share by Platform", fontweight='bold')
chart_files['platform_pie'] = os.path.join(CHARTS_DIR, "4_platform_pie.png")
fig.savefig(chart_files['platform_pie'], dpi=200)
plt.close(fig)

# Chart 5: Monthly Trend
fig, ax = plt.subplots(figsize=(6, 3.5))
monthly = df.groupby('post_month')['total_engagement'].sum().reset_index()
sns.lineplot(data=monthly, x='post_month', y='total_engagement', marker='o', color='#DC2626', ax=ax)
ax.set_title("Monthly Total Engagement Trend", fontweight='bold')
ax.set_xlabel("Month")
ax.set_ylabel("Total Engagement")
plt.xticks(rotation=45)
chart_files['monthly_trend'] = os.path.join(CHARTS_DIR, "5_monthly_trend.png")
fig.savefig(chart_files['monthly_trend'], dpi=200)
plt.close(fig)

# Chart 6: Scatter Plot (Impressions vs Total Engagement)
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.scatterplot(data=df, x='impressions', y='total_engagement', hue='platform', alpha=0.7, ax=ax)
ax.set_title("Impressions vs. Total Engagement", fontweight='bold')
ax.set_xlabel("Impressions")
ax.set_ylabel("Total Engagement")
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=8)
chart_files['scatter'] = os.path.join(CHARTS_DIR, "6_scatter_reach_eng.png")
fig.savefig(chart_files['scatter'], dpi=200)
plt.close(fig)

# Chart 7: Box Plot (Likes by Platform)
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.boxplot(data=df, x='platform', y='likes_count', palette='Set2', ax=ax)
ax.set_title("Likes Dispersion Across Platforms", fontweight='bold')
ax.set_xlabel("Platform")
ax.set_ylabel("Likes")
chart_files['boxplot'] = os.path.join(CHARTS_DIR, "7_boxplot_likes.png")
fig.savefig(chart_files['boxplot'], dpi=200)
plt.close(fig)

# Chart 8: Correlation Heatmap
fig, ax = plt.subplots(figsize=(6, 3.5))
corr_matrix = df[['likes_count', 'comments_count', 'shares_count', 'impressions', 'total_engagement']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True, ax=ax, annot_kws={"size": 8})
ax.set_title("Engagement Metric Correlations", fontweight='bold')
chart_files['heatmap'] = os.path.join(CHARTS_DIR, "8_corr_heatmap.png")
fig.savefig(chart_files['heatmap'], dpi=200)
plt.close(fig)

print("All charts generated.")

# -------------------------------------------------------------------------
# 3. Calculate Core KPI Summary & Tables
# -------------------------------------------------------------------------
total_posts = len(df)
total_engagement = int(df['total_engagement'].sum())
avg_likes = df['likes_count'].mean()
avg_comments = df['comments_count'].mean()
total_impressions = int(df['impressions'].sum())
overall_eng_rate = (total_engagement / total_impressions * 100) if total_impressions > 0 else 0

platform_grp = df.groupby('platform').agg(
    Posts=('post_id', 'count'),
    Avg_Likes=('likes_count', 'mean'),
    Avg_Comments=('comments_count', 'mean'),
    Total_Eng=('total_engagement', 'sum')
).reset_index()

# -------------------------------------------------------------------------
# 4. Build Professional PDF Report
# -------------------------------------------------------------------------
print("Compiling PDF report...")

class AnalyticsReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 41, 59)
        self.cell(0, 8, 'Executive Social Media Analytics & Strategy Report', border=False, align='L')
        self.ln(6)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, 'Comprehensive Campaign Performance & Content Strategy Analysis', border='B', align='L')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = AnalyticsReport(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)

# ----------------- PAGE 1: Executive Summary & Platform Table -----------------
pdf.add_page()

# KPI Banner Header
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 6, 'Executive Performance Scorecard', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)

# Render KPI grid (6 metrics)
pdf.set_fill_color(248, 250, 252)
pdf.set_draw_color(226, 232, 240)
kpis = [
    ("Total Posts", f"{total_posts:,}"),
    ("Total Engagement", f"{total_engagement:,}"),
    ("Total Impressions", f"{total_impressions:,}"),
    ("Average Likes", f"{avg_likes:.1f}"),
    ("Average Comments", f"{avg_comments:.1f}"),
    ("Engagement Rate", f"{overall_eng_rate:.2f}%")
]

card_w = 60
card_h = 14
x_start = pdf.get_x()
y_start = pdf.get_y()

for i, (title, val) in enumerate(kpis):
    col_idx = i % 3
    row_idx = i // 3
    pdf.set_xy(x_start + (col_idx * 64), y_start + (row_idx * 16))
    pdf.rect(pdf.get_x(), pdf.get_y(), card_w, card_h, 'DF')
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(card_w, 5, title, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(x_start + (col_idx * 64))
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(card_w, 7, val, align='C')

pdf.set_xy(x_start, y_start + 36)

# Platform Performance Summary Table
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 6, 'Platform Aggregate Performance', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)

pdf.set_font('Helvetica', 'B', 8)
pdf.set_fill_color(241, 245, 249)
pdf.set_text_color(51, 65, 85)
col_widths = [45, 35, 35, 35, 40]
headers = ['Platform', 'Post Count', 'Avg Likes', 'Avg Comments', 'Total Engagement']

for w, h in zip(col_widths, headers):
    pdf.cell(w, 7, h, border=1, align='C', fill=True)
pdf.ln()

pdf.set_font('Helvetica', '', 8)
pdf.set_text_color(30, 41, 59)
for _, row in platform_grp.iterrows():
    pdf.cell(col_widths[0], 6, str(row['platform']), border=1)
    pdf.cell(col_widths[1], 6, f"{int(row['Posts']):,}", border=1, align='R')
    pdf.cell(col_widths[2], 6, f"{row['Avg_Likes']:.1f}", border=1, align='R')
    pdf.cell(col_widths[3], 6, f"{row['Avg_Comments']:.1f}", border=1, align='R')
    pdf.cell(col_widths[4], 6, f"{int(row['Total_Eng']):,}", border=1, align='R')
    pdf.ln()

pdf.ln(6)

# Insert First Pair of Visualizations
pdf.image(chart_files['platform_bar'], x=12, y=pdf.get_y(), w=90)
pdf.image(chart_files['platform_pie'], x=108, y=pdf.get_y(), w=90)

# ----------------- PAGE 2: Engagement Trends & Distributions -----------------
pdf.add_page()
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 6, 'Audience Interaction & Distribution Dynamics', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)

current_y = pdf.get_y()
pdf.image(chart_files['likes_dist'], x=12, y=current_y, w=90)
pdf.image(chart_files['comments_dist'], x=108, y=current_y, w=90)

pdf.set_y(current_y + 60)
current_y = pdf.get_y()
pdf.image(chart_files['monthly_trend'], x=12, y=current_y, w=90)
pdf.image(chart_files['scatter'], x=108, y=current_y, w=90)

pdf.set_y(current_y + 60)
current_y = pdf.get_y()
pdf.image(chart_files['boxplot'], x=12, y=current_y, w=90)
pdf.image(chart_files['heatmap'], x=108, y=current_y, w=90)

# ----------------- PAGE 3: Business Insights & Strategy -----------------
pdf.add_page()
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 6, 'Data-Driven Business Insights', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)

top_platform_row = platform_grp.sort_values(by='Total_Eng', ascending=False).iloc[0]
corr_val = df['impressions'].corr(df['total_engagement'])

insights = [
    f"Primary Driver: '{top_platform_row['platform']}' delivers the largest interaction volume, driving {int(top_platform_row['Total_Eng']):,} total actions across {int(top_platform_row['Posts'])} posts.",
    f"Impression Elasticity: The correlation coefficient between impressions and total engagement is {corr_val:.2f}. " + 
    ("Strong reach correlation suggests broad targeting drives action." if corr_val > 0.5 else "Moderate to low correlation highlights that creative hooks and contextual relevance drive engagement far more than raw reach alone."),
    f"Action Ratio: Average likes ({avg_likes:.1f}) dominate user response patterns compared to comments ({avg_comments:.1f}), emphasizing passive endorsement over community dialogue across default formats."
]

pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(51, 65, 85)
for ins in insights:
    pdf.multi_cell(0, 5, f"-  {ins}")
    pdf.ln(2)

pdf.ln(4)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 6, 'Strategic Marketing Recommendations', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)

recommendations = [
    ("Shift Budget to Top-Performing Channels", 
     f"Reallocate 20-30% of underperforming platform spend directly into {top_platform_row['platform']} campaigns to maximize ROI per dollar spent."),
    ("Incentivize Comment Generation", 
     "Passive likes do not trigger platform algorithmic amplification as effectively as active comments. Implement interactive prompts, polls, and open discussions to double comment rates."),
    ("Optimize Frequency Based on Dispersion", 
     "Variance in the likes distribution indicates high volatility in post reach. Standardize content templates to maintain quality and minimize underperforming outliers."),
    ("Re-evaluate Paid Impressions", 
     "Ensure programmatic ad campaigns focus on quality target personas rather than broad impressions, preserving budget for conversion-focused content.")
]

for title, rec in recommendations:
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, f"* {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 4.5, rec)
    pdf.ln(2)

# Output PDF
pdf.output(PDF_OUTPUT_PATH)
print(f"Report compiled successfully: {PDF_OUTPUT_PATH}")