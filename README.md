# CodeAlpha Data Analytics Internship Projects

This repository contains the projects completed as part of the **CodeAlpha Data Analytics Internship**. 

It contains implementations for all **four core tasks** using Python:
1. **Task 1: Web Scraping**
2. **Task 2: Exploratory Data Analysis (EDA)**
3. **Task 3: Data Visualization**
4. **Task 4: Sentiment Analysis**

---

## 📁 Repository Structure

```text
CodeAlpha Internship/
│
├── task1_web_scraping/
│   ├── scrape_books.py                # Python web scraper script
│   └── raw_books_data.csv             # Scraped books raw dataset
│
├── task2_eda/
│   ├── eda_books.py                   # Exploratory Data Analysis script
│   └── cleaned_books_data.csv         # Cleaned books dataset
│
├── task3_visualization/
│   ├── visualize_books.py             # Data visualization script
│   ├── dashboard.html                 # Premium Web Analytics Dashboard (Double-click to open)
│   └── plots/                         # Saved visualizations and charts
│       ├── price_distribution.png
│       ├── ratings_count.png
│       ├── top_expensive_categories.png
│       └── price_vs_rating_boxplot.png
│
├── task4_sentiment_analysis/
│   ├── sentiment_analysis.py          # Custom lexicon Sentiment analysis script
│   ├── reviews_data.csv               # Input reviews dataset
│   ├── reviews_sentiment_results.csv  # Sentiment scoring output CSV
│   └── plots/                         # Saved sentiment charts
│       ├── sentiment_distribution.png
│       └── sentiment_vs_rating.png
│
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/CodeAlpha_Data_Analytics.git
   cd CodeAlpha_Data_Analytics
   ```

2. **Install dependencies**:
   Make sure you have Python 3.8+ installed. Run the following command to install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run the Tasks

You can run each task sequentially to see the full data pipeline from scraping to visualization:

### Task 1: Web Scraping
This script scrapes details of books (Title, Price, Star Rating, Availability, Category) across all categories from the sandbox website [books.toscrape.com](http://books.toscrape.com/) and saves the data to a CSV.
```bash
python task1_web_scraping/scrape_books.py
```

### Task 2: Exploratory Data Analysis (EDA)
This script loads the raw book data, cleans it (removing duplicates, trimming text, correcting pricing data types), computes key statistics (averages, rating distributions, and category comparisons), and saves a cleaned dataset.
```bash
python task2_eda/eda_books.py
```

### Task 3: Data Visualization
This script creates and saves four premium, publication-quality visualizations using `matplotlib` and `seaborn` based on the cleaned books data. It also compiles them into an interactive and responsive HTML dashboard page ([dashboard.html](file:///c:/Users/PC/OneDrive/Desktop/CodeAlpha%20Internship/task3_visualization/dashboard.html)) that can be opened directly in any browser.
```bash
python task3_visualization/visualize_books.py
```

### Task 4: Sentiment Analysis
This script performs sentiment analysis on a dataset of customer reviews using a custom offline rule-based lexicon analyzer (optimized for Python 3.13 and running fully offline without internet download issues). It classifies reviews into Positive, Neutral, and Negative sentiments and saves the results along with sentiment distribution plots.
```bash
python task4_sentiment_analysis/sentiment_analysis.py
```

---

## 📊 Summary of Insights & Outputs

### Books Dataset Analysis (Tasks 1-3)
- **Average Price**: The average price of books across all categories is approximately **£35.07**.
- **Ratings**: Book ratings are distributed fairly evenly across categories, with a slight variation in prices across different star ratings.
- **Top Categories**: Categories like *Travel*, *Nonfiction*, and *Sequential Art* are highly popular, while average prices vary significantly by category.

### Sentiment Analysis (Task 4)
- Sentiment analysis of customer reviews highlights a direct correlation between star ratings and the computed lexicon sentiment score.
- The majority of 5-star reviews score high in compound score (positive), while 1-star reviews successfully align with negative scores.

---

## 🏆 Key Technologies Used
- **Language**: Python 3
- **Libraries**:
  - `requests` & `BeautifulSoup4` (Web Scraping)
  - `pandas` (Data Manipulation & Cleaning)
  - `matplotlib` & `seaborn` (Data Visualization)
  - `nltk` (Natural Language Processing & Sentiment Analysis)
