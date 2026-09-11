import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_report(analysis, chart_output_dir, report_output_path):
    c = canvas.Canvas(report_output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Social Media Engagement Analysis Report")
    
    # Summary Insights
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 80, f"Total Posts Analyzed: {analysis['overall']['total_posts']}")
    c.drawString(50, height - 100, f"Average Global Engagement Rate: {analysis['overall']['avg_engagement_rate']}%")
    c.drawString(50, height - 120, f"Top Performing Platform: {analysis['overall']['top_performing_platform']}")
    c.drawString(50, height - 140, f"Best Content Format: {analysis['overall']['top_performing_content']}")
    
    # Insert Chart 1
    chart1 = os.path.join(chart_output_dir, "platform_engagement.png")
    if os.path.exists(chart1):
        c.drawImage(chart1, 50, height - 420, width=500, height=260)
        
    # Page 2
    c.showPage()
    
    # Insert Chart 2 & 3
    chart2 = os.path.join(chart_output_dir, "content_engagements.png")
    if os.path.exists(chart2):
        c.drawImage(chart2, 50, height - 320, width=500, height=250)
        
    chart3 = os.path.join(chart_output_dir, "correlation_heatmap.png")
    if os.path.exists(chart3):
        c.drawImage(chart3, 50, height - 600, width=400, height=260)
        
    c.save()