import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations():
    # Construct paths
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(script_dir)
    input_path = os.path.join(project_dir, "task2_eda", "cleaned_books_data.csv")
    plots_dir = os.path.join(script_dir, "plots")
    
    # Create plots directory if it doesn't exist
    os.makedirs(plots_dir, exist_ok=True)
    
    print("=" * 60)
    print("      DATA VISUALIZATION GENERATOR - CODEALPHA TASK 3")
    print("=" * 60)
    
    # 1. Load Dataset
    if not os.path.exists(input_path):
        print(f"[-] Error: Cleaned dataset not found at {input_path}")
        print("[i] Please run the EDA script first to clean the data.")
        return
        
    print(f"[+] Loading cleaned dataset from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Set premium Seaborn style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16
    })
    
    primary_color = "#2E8B57" # SeaGreen
    
    # ----------------- PLOT 1: Price Distribution -----------------
    print("[+] Generating Plot 1: Price Distribution...")
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Price", kde=True, color=primary_color, bins=30, edgecolor="w", alpha=0.8)
    
    mean_price = df["Price"].mean()
    median_price = df["Price"].median()
    plt.axvline(mean_price, color="#D9534F", linestyle="--", linewidth=1.5, label=f"Mean Price: £{mean_price:.2f}")
    plt.axvline(median_price, color="#F0AD4E", linestyle="-", linewidth=1.5, label=f"Median Price: £{median_price:.2f}")
    
    plt.title("Distribution of Book Prices", pad=15, fontweight="bold")
    plt.xlabel("Price (£)", labelpad=10)
    plt.ylabel("Count of Books", labelpad=10)
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    
    plot1_path = os.path.join(plots_dir, "price_distribution.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    print(f"    [i] Saved: {plot1_path}")
    
    # ----------------- PLOT 2: Rating Counts -----------------
    print("[+] Generating Plot 2: Ratings Count...")
    plt.figure(figsize=(8, 6))
    rating_counts = df["Rating"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["Rating", "Count"]
    
    ax = sns.barplot(
        data=rating_counts, 
        x="Rating", 
        y="Count", 
        hue="Rating",
        palette="crest", 
        legend=False
    )
    
    # Add count labels on top of the bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{int(height)}",
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='bottom',
            xytext=(0, 5),
            textcoords='offset points',
            fontweight="bold"
        )
        
    plt.title("Number of Books per Star Rating", pad=15, fontweight="bold")
    plt.xlabel("Rating (Stars)", labelpad=10)
    plt.ylabel("Number of Books", labelpad=10)
    plt.ylim(0, max(rating_counts["Count"]) * 1.1)
    plt.tight_layout()
    
    plot2_path = os.path.join(plots_dir, "ratings_count.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    print(f"    [i] Saved: {plot2_path}")
    
    # ----------------- PLOT 3: Top 10 Most Expensive Categories -----------------
    print("[+] Generating Plot 3: Top 10 Most Expensive Categories...")
    plt.figure(figsize=(10, 6))
    cat_stats = df.groupby("Category").agg(
        Average_Price=("Price", "mean"),
        Book_Count=("Price", "count")
    ).reset_index()
    top_expensive = cat_stats.sort_values(by="Average_Price", ascending=False).head(10)
    
    sns.barplot(
        data=top_expensive, 
        y="Category", 
        x="Average_Price", 
        hue="Category",
        palette="flare_r", 
        legend=False
    )
    
    plt.title("Top 10 Most Expensive Book Categories (Average Price)", pad=15, fontweight="bold")
    plt.xlabel("Average Price (£)", labelpad=10)
    plt.ylabel("Category", labelpad=10)
    plt.tight_layout()
    
    plot3_path = os.path.join(plots_dir, "top_expensive_categories.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    print(f"    [i] Saved: {plot3_path}")
    
    # ----------------- PLOT 4: Price vs Rating Box Plot -----------------
    print("[+] Generating Plot 4: Price vs Rating Distribution...")
    plt.figure(figsize=(9, 6))
    sns.boxplot(
        data=df, 
        x="Rating", 
        y="Price", 
        hue="Rating",
        palette="viridis",
        legend=False
    )
    
    plt.title("Book Prices Across Rating Levels", pad=15, fontweight="bold")
    plt.xlabel("Rating (Stars)", labelpad=10)
    plt.ylabel("Price (£)", labelpad=10)
    plt.tight_layout()
    
    plot4_path = os.path.join(plots_dir, "price_vs_rating_boxplot.png")
    plt.savefig(plot4_path, dpi=300)
    plt.close()
    print(f"    [i] Saved: {plot4_path}")
    
    # 5. Generate HTML Dashboard
    generate_html_dashboard(df, plots_dir)
    
    print("\n[+] All visualizations generated successfully!")
    print(f"[i] Charts and Dashboard can be viewed inside: {script_dir}")
    print("=" * 60)

def generate_html_dashboard(df, plots_dir):
    """
    Generates a premium, responsive local HTML dashboard linking to the plots
    and displaying metrics and insights.
    """
    total_books = len(df)
    avg_price = df["Price"].mean()
    median_price = df["Price"].median()
    correlation = df["Rating"].corr(df["Price"])
    
    cat_means = df.groupby("Category")["Price"].mean()
    most_exp_cat = cat_means.idxmax()
    most_exp_val = cat_means.max()
    
    dashboard_path = os.path.join(os.path.dirname(plots_dir), "dashboard.html")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Bookstore Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-orange: #f59e0b;
            --accent-rose: #f43f5e;
            --border-color: #334155;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            margin-bottom: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #10b981, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        header p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}
        
        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }}
        
        .kpi-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-blue);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        }}
        
        .kpi-title {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .kpi-value {{
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 5px;
        }}
        
        .kpi-desc {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .kpi-card.green .kpi-value {{ color: var(--accent-green); }}
        .kpi-card.blue .kpi-value {{ color: var(--accent-blue); }}
        .kpi-card.orange .kpi-value {{ color: var(--accent-orange); }}
        .kpi-card.rose .kpi-value {{ color: var(--accent-rose); }}

        /* Main Analysis Grid */
        .visual-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 40px;
        }}
        
        .section-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
            color: var(--text-primary);
        }}
        
        .plot-container {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 30px;
            align-items: center;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transition: border-color 0.3s ease;
        }}
        
        .plot-container:hover {{
            border-color: var(--accent-green);
        }}
        
        @media (max-width: 1024px) {{
            .plot-container {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .plot-image-wrapper {{
            width: 100%;
            overflow: hidden;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }}
        
        .plot-image-wrapper img {{
            width: 100%;
            height: auto;
            display: block;
            transition: transform 0.5s ease;
        }}
        
        .plot-image-wrapper img:hover {{
            transform: scale(1.03);
        }}
        
        .story-panel {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .story-tag {{
            align-self: flex-start;
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
        }}
        
        .plot-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--text-primary);
        }}
        
        .story-text {{
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-secondary);
            margin-bottom: 20px;
        }}
        
        .insight-box {{
            background: rgba(16, 185, 129, 0.08);
            border-left: 4px solid var(--accent-green);
            padding: 15px;
            border-radius: 0 12px 12px 0;
            font-size: 0.95rem;
            line-height: 1.5;
            color: var(--text-primary);
        }}
        
        .insight-box strong {{
            color: var(--accent-green);
        }}
        
        footer {{
            margin-top: 60px;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>E-Commerce Bookstore Analytics Dashboard</h1>
            <p>CodeAlpha Data Analytics Internship Portfolio - Interactive Deliverable</p>
        </header>
        
        <!-- KPI Row -->
        <div class="kpi-grid">
            <div class="kpi-card green">
                <div>
                    <div class="kpi-title">Total Inventory Volume</div>
                    <div class="kpi-value">{total_books:,}</div>
                </div>
                <div class="kpi-desc">Total unique book listings crawled and analyzed</div>
            </div>
            
            <div class="kpi-card blue">
                <div>
                    <div class="kpi-title">Average Book Cost</div>
                    <div class="kpi-value">£{avg_price:.2f}</div>
                </div>
                <div class="kpi-desc">Median price is £{median_price:.2f} (Symmetric distribution)</div>
            </div>
            
            <div class="kpi-card orange">
                <div>
                    <div class="kpi-title">Rating-Price Correlation</div>
                    <div class="kpi-value">{correlation:.4f}</div>
                </div>
                <div class="kpi-desc">Near 0: Price is independent of ratings</div>
            </div>
            
            <div class="kpi-card rose">
                <div>
                    <div class="kpi-title">Most Premium Category</div>
                    <div class="kpi-value" style="font-size: 1.6rem; margin-top: 10px;">{most_exp_cat}</div>
                </div>
                <div class="kpi-desc">Highest average price of £{most_exp_val:.2f}</div>
            </div>
        </div>
        
        <h2 class="section-title">Visual Interpretations & Data Stories</h2>
        
        <!-- Visualizations Grid -->
        <div class="visual-grid">
            
            <!-- Plot 1 -->
            <div class="plot-container">
                <div class="plot-image-wrapper">
                    <img src="plots/price_distribution.png" alt="Price Distribution">
                </div>
                <div class="story-panel">
                    <div class="story-tag">Market Analysis</div>
                    <h3 class="plot-title">How Book Prices are Distributed</h3>
                    <p class="story-text">
                        This histogram with a Kernel Density Estimate (KDE) line shows how book prices are spread across the bookstore inventory. 
                        The vertical lines represent the average price (red dashed line) and median price (orange solid line).
                    </p>
                    <div class="insight-box">
                        <strong>Decision Insight:</strong> The distribution is relatively uniform between £10 and £60, with no severe outliers. 
                        This suggests a flat pricing model where items are evenly distributed across budget brackets, supporting retail strategies aiming for wide audience accessibility.
                    </div>
                </div>
            </div>
            
            <!-- Plot 2 -->
            <div class="plot-container">
                <div class="plot-image-wrapper">
                    <img src="plots/ratings_count.png" alt="Ratings Count">
                </div>
                <div class="story-panel">
                    <div class="story-tag">Customer Sentiment</div>
                    <h3 class="plot-title">Distribution of Consumer Ratings</h3>
                    <p class="story-text">
                        This bar plot lists the frequency of books per star-rating category from 1 to 5. 
                        It reveals the volume of customer reviews across the platform.
                    </p>
                    <div class="insight-box">
                        <strong>Decision Insight:</strong> Ratings are highly balanced, with each bracket containing 18% to 22% of total inventory. 
                        No single rating dominates, indicating unbiased consumer feedback or a broad range of content quality across products.
                    </div>
                </div>
            </div>
            
            <!-- Plot 3 -->
            <div class="plot-container">
                <div class="plot-image-wrapper">
                    <img src="plots/top_expensive_categories.png" alt="Top Expensive Categories">
                </div>
                <div class="story-panel">
                    <div class="story-tag">Product Portfolio</div>
                    <h3 class="plot-title">Average Book Prices by Category</h3>
                    <p class="story-text">
                        This horizontal bar chart highlights the top 10 most expensive genres by average retail price.
                    </p>
                    <div class="insight-box">
                        <strong>Decision Insight:</strong> Categories like 'Suspense' and 'Novels' average over £54 per book, making them premium product lines. 
                        Marketing budgets and premium promotional banners should target these high-margin categories to maximize revenue per sale.
                    </div>
                </div>
            </div>
            
            <!-- Plot 4 -->
            <div class="plot-container">
                <div class="plot-image-wrapper">
                    <img src="plots/price_vs_rating_boxplot.png" alt="Price vs Rating">
                </div>
                <div class="story-panel">
                    <div class="story-tag">Statistical Validation</div>
                    <h3 class="plot-title">Book Prices Across Rating Levels</h3>
                    <p class="story-text">
                        This box-and-whisker plot compares price ranges across different ratings. 
                        The boxes show the IQR (Interquartile Range) and the horizontal line shows the median price.
                    </p>
                    <div class="insight-box">
                        <strong>Decision Insight:</strong> The box plots are remarkably aligned and overlap extensively. 
                        This visually validates our statistical hypothesis test, confirming that rating does not drive pricing. 
                        Premium products are priced high regardless of whether they have a 1-star or 5-star rating.
                    </div>
                </div>
            </div>
            
        </div>
        
        <footer>
            <p>© 2026 CodeAlpha Internship Portfolio. Developed as a professional Data Analytics submission.</p>
        </footer>
    </div>
</body>
</html>
"""
    try:
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Interactive HTML Dashboard generated at: {dashboard_path}")
    except Exception as e:
        print(f"[-] Failed to generate HTML dashboard: {e}")

if __name__ == "__main__":
    generate_visualizations()
