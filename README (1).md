# 🛍️ Shoppers Spectrum: AI-Powered Retail Analytics

Shoppers Spectrum is an end-to-end data science project that transforms raw e-commerce transactional data into actionable business intelligence. It features a live interactive dashboard that tracks sales performance, segments customers using **K-Means Clustering**, and suggests products via a **Recommendation Engine**.



## 🚀 Live Demo
*Link your deployed app here once it's live:* 👉 [View Interactive Dashboard](https://your-app-name.streamlit.app/)

## 🛠️ Features
- **Interactive Sales Dashboard**: Real-time filtering by country and date to monitor Revenue, Average Order Value, and Sales Trends.
- **Customer Segmentation (RFM)**: Uses Machine Learning (K-Means) to group customers into personas based on Recency, Frequency, and Monetary value.
- **AI Recommendation Engine**: Implements **Cosine Similarity** to provide "Frequently Bought Together" product suggestions.
- **Optimized Data Pipeline**: Handles large datasets efficiently using Gzip compression and cached data loading.

## 📁 Project Structure
```text
├── app.py                       # Main Streamlit dashboard interface
├── cleaning_eda.py              # Data processing and AI model generation script
├── cleaned_online_retail.csv.gz # Compressed transaction data
├── rfm.csv                      # Customer segmentation results
├── product_similarity_matrix.csv # AI Recommendation lookup table
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
