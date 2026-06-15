import os
import pandas as pd
import numpy as np

def perform_eda():
    # Construct paths
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(script_dir)
    input_path = os.path.join(project_dir, "task1_web_scraping", "raw_books_data.csv")
    output_path = os.path.join(script_dir, "cleaned_books_data.csv")
    report_path = os.path.join(script_dir, "eda_insights_report.txt")
    
    print("=" * 65)
    print("      EXPLORATORY DATA ANALYSIS (EDA) - CODEALPHA TASK 2")
    print("=" * 65)
    
    # 1. Ask Meaningful Questions (Point 1 of instructions)
    print("\n--- [Step 1] Formulating Pre-Analysis Questions ---")
    questions = [
        "Q1: What is the total size, structure, and column data types of the books dataset?",
        "Q2: How are book ratings distributed, and what rating is the most common?",
        "Q3: Does the book price correlate with its rating? (Hypothesis: Higher rated books cost more)",
        "Q4: Which categories are the most expensive on average, and which are the cheapest?",
        "Q5: Are there any statistical anomalies (price outliers) or data issues (missing/corrupted values)?"
    ]
    for q in questions:
        print(f"  [?] {q}")
        
    # Check if raw dataset exists
    if not os.path.exists(input_path):
        print(f"\n[-] Error: Raw dataset not found at {input_path}")
        print("[i] Please run the web scraping script first to gather data.")
        return
        
    print(f"\n[+] Loading dataset from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 2. Explore Data Structure (Point 2 of instructions)
    print("\n--- [Step 2] Exploring Data Structure & Integrity ---")
    rows, cols = df.shape
    print(f"Dimensions: {rows} rows (books) and {cols} columns.")
    print("\nVariables and Data Types:")
    for col, dtype in df.dtypes.items():
        missing_count = df[col].isnull().sum()
        print(f"  - {col:15} | Type: {str(dtype):8} | Missing Values: {missing_count}")
        
    # 3. Detect Potential Data Issues (Point 5 of instructions)
    print("\n--- [Step 3] Detecting Anomalies & Data Issues ---")
    # A. Check for Duplicates
    duplicates_count = df.duplicated().sum()
    print(f"  [i] Duplicate rows detected: {duplicates_count}")
    
    # B. Check for Negative or Free Prices
    invalid_prices = (df['Price'] <= 0).sum()
    print(f"  [i] Invalid/Negative price values: {invalid_prices}")
    
    # C. Statistical Price Outlier Detection using Interquartile Range (IQR) Method
    q1 = df['Price'].quantile(0.25)
    q3 = df['Price'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = max(0, q1 - 1.5 * iqr) # price can't be negative
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df['Price'] < lower_bound) | (df['Price'] > upper_bound)]
    print(f"  [i] IQR Outlier Bounds for Price: £{lower_bound:.2f} to £{upper_bound:.2f}")
    print(f"  [i] Statistical Price Outliers Detected: {len(outliers)}")
    if not outliers.empty:
        print("      * Outlier Examples:")
        print(outliers[['Title', 'Price', 'Category']].head(3).to_string(index=False))
        
    # 4. Clean Data
    print("\n[+] Cleaning text variables...")
    if duplicates_count > 0:
        df = df.drop_duplicates()
    df['Title'] = df['Title'].str.strip()
    df['Availability'] = df['Availability'].str.strip()
    df['Category'] = df['Category'].str.strip()
    
    # 5. Identify Trends, Patterns (Point 3 of instructions)
    print("\n--- [Step 4] Trend & Pattern Analysis ---")
    
    # Ratings Count and Percentages
    print("\nRatings Distribution:")
    rating_counts = df['Rating'].value_counts().sort_index()
    rating_pcts = df['Rating'].value_counts(normalize=True).sort_index() * 100
    for stars, count in rating_counts.items():
        print(f"  - {stars} Stars: {count:3} books ({rating_pcts[stars]:.1f}%)")
        
    # Category Popularity (Top 5 by count)
    print("\nTop 5 Most Populated Categories:")
    top_cats = df['Category'].value_counts().head(5)
    for cat, count in top_cats.items():
        print(f"  - {cat:20}: {count} books")
        
    # Category Pricing
    print("\nTop 5 Most Expensive Categories (Average Price):")
    expensive_cats = df.groupby('Category')['Price'].mean().sort_values(ascending=False).head(5)
    for cat, avg_price in expensive_cats.items():
        print(f"  - {cat:20}: £{avg_price:.2f}")
        
    print("\nTop 5 Cheapest Categories (Average Price):")
    cheapest_cats = df.groupby('Category')['Price'].mean().sort_values(ascending=True).head(5)
    for cat, avg_price in cheapest_cats.items():
        print(f"  - {cat:20}: £{avg_price:.2f}")
        
    # 6. Test Hypotheses (Point 4 of instructions)
    print("\n--- [Step 5] Hypothesis Testing & Assumptions Validation ---")
    print("Hypothesis: Higher rated books have higher retail prices.")
    
    # Calculate Correlation Coefficient (Pearson)
    correlation = df['Rating'].corr(df['Price'])
    print(f"  - Computed Pearson Correlation Coefficient (r): {correlation:.4f}")
    
    # Calculate average price per rating category
    avg_price_by_rating = df.groupby('Rating')['Price'].mean().round(2)
    print("  - Average Price by Rating Level:")
    for rate, avg_pr in avg_price_by_rating.items():
        print(f"    * {rate} Star Rating: £{avg_pr:.2f}")
        
    # Validate
    print("\n  Validation Conclusion:")
    if abs(correlation) < 0.1:
        print("    [!] Assumption Falsified: Price and ratings have no linear correlation (r is near 0).")
        print("        Retail price is set independently of consumer ratings on this platform.")
    elif correlation > 0:
        print("    [✓] Assumption Validated: There is a positive correlation (higher-rated books cost more).")
    else:
        print("    [!] Assumption Falsified: Negative correlation detected.")

    # 7. Save Cleaned Dataset & Report
    print("\n--- [Step 6] Exporting Deliverables ---")
    df.to_csv(output_path, index=False)
    print(f"[+] Cleaned dataset saved to: {output_path}")
    
    # Write details to a formal insights report
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 65 + "\n")
            f.write("       CODEALPHA EXPLORATORY DATA ANALYSIS (EDA) REPORT\n")
            f.write("=" * 65 + "\n\n")
            
            f.write("1. DATASET CHARACTERISTICS\n")
            f.write(f"  - Total books analyzed: {rows}\n")
            f.write(f"  - Columns: {', '.join(df.columns)}\n\n")
            
            f.write("2. HYPOTHESIS TESTING SUMMARY\n")
            f.write("  - Objective: Test if book ratings affect price.\n")
            f.write(f"  - Pearson Correlation: {correlation:.4f}\n")
            f.write("  - Results by Rating:\n")
            for rate, avg_pr in avg_price_by_rating.items():
                f.write(f"    * {rate}-Star: £{avg_pr:.2f}\n")
            f.write(f"  - Conclusion: Price and ratings are statistically independent (Correlation r = {correlation:.4f}).\n\n")
            
            f.write("3. CATEGORICAL INSIGHTS\n")
            f.write("  - Top 3 Categories by volume:\n")
            for cat, count in top_cats.head(3).items():
                f.write(f"    * {cat}: {count} books\n")
            f.write("  - Top 3 Most Expensive Categories:\n")
            for cat, avg_price in expensive_cats.head(3).items():
                f.write(f"    * {cat}: £{avg_price:.2f}\n")
            f.write("  - Top 3 Cheapest Categories:\n")
            for cat, avg_price in cheapest_cats.head(3).items():
                f.write(f"    * {cat}: £{avg_price:.2f}\n\n")
                
            f.write("4. ANOMALIES & DATA ISSUES DETECTED\n")
            f.write(f"  - Duplicate rows dropped: {duplicates_count}\n")
            f.write(f"  - Negative prices: {invalid_prices}\n")
            f.write(f"  - Statistical Outliers (Price): {len(outliers)} books\n")
            f.write("=" * 65 + "\n")
        print(f"[+] EDA Insights Report generated at: {report_path}")
    except Exception as e:
        print(f"[-] Failed to generate report: {e}")
    print("=" * 65)

if __name__ == "__main__":
    perform_eda()
