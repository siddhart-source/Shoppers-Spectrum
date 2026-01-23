import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shoppers Spectrum AI", layout="wide", page_icon="🛍️")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border: 1px solid #e1e4e8; padding: 15px; border-radius: 10px; background-color: white; }
    div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_all_data():
    sales = pd.read_csv('cleaned_online_retail.csv.gz')
    sales['InvoiceDate'] = pd.to_datetime(sales['InvoiceDate'])
    
    rfm = pd.read_csv('rfm.csv')
    
    # Load Similarity Matrix (index_col=0 ensures the StockCodes are the row labels)
    similarity = pd.read_csv('product_similarity_matrix.csv', index_col=0)
    
    return sales, rfm, similarity

try:
    df, rfm, similarity = load_all_data()
    # Create a mapping for Recommendation Engine
    item_map = df[['StockCode', 'Description']].drop_duplicates().set_index('StockCode')['Description'].to_dict()
    desc_to_code = {v: k for k, v in item_map.items()}
except Exception as e:
    st.error(f"Error loading files: {e}. Ensure 'cleaned_online_retail.csv', 'rfm.csv', and 'product_similarity_matrix.csv' are in the same folder.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("🔍 Project Filters")
country_list = ["All"] + list(df['Country'].unique())
selected_country = st.sidebar.selectbox("Market Selection", country_list)

if selected_country != "All":
    filtered_df = df[df['Country'] == selected_country]
else:
    filtered_df = df

# --- TABS ---
st.title("🛍️ Shoppers Spectrum: AI-Driven Retail Insights")
tab1, tab2, tab3 = st.tabs(["📊 Business Overview", "👥 Customer Segments", "💡 AI Recommendations"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.subheader(f"Performance Analysis: {selected_country}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue", f"${filtered_df['TotalPrice'].sum():,.0f}")
    m2.metric("Orders", f"{filtered_df['InvoiceNo'].nunique():,}")
    m3.metric("Avg. Order", f"${filtered_df.groupby('InvoiceNo')['TotalPrice'].sum().mean():,.2f}")
    m4.metric("Customers", f"{filtered_df['CustomerID'].nunique():,}")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("### Sales Trend")
        trend = filtered_df.set_index('InvoiceDate').resample('M')['TotalPrice'].sum().reset_index()
        st.plotly_chart(px.line(trend, x='InvoiceDate', y='TotalPrice', template="plotly_white"), use_container_width=True)
    with col2:
        st.write("### Top Sellers")
        top_p = filtered_df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
        st.plotly_chart(px.bar(top_p, x='Quantity', y='Description', orientation='h', color_continuous_scale='Blues'), use_container_width=True)

# --- TAB 2: SEGMENTS ---
with tab2:
    st.header("Customer Clustering (RFM)")
    if 'Cluster' in rfm.columns:
        fig_cluster = px.scatter(rfm, x="Recency", y="Monetary", color=rfm["Cluster"].astype(str), 
                                 size="Frequency", hover_name="CustomerID", title="Customer Personas",
                                 color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_cluster, use_container_width=True)
    else:
        st.info("RFM data loaded. Cluster visualizations will appear once 'Cluster' column is detected.")
        st.dataframe(rfm.head())

# --- TAB 3: RECOMMENDATIONS ---
with tab3:
    st.header("AI Product Recommendation Engine")
    st.write("This engine uses **Cosine Similarity** from your matrix to find products often bought together.")
    
    # Filter descriptions that actually exist in the similarity matrix
    valid_descriptions = [item_map[code] for code in similarity.index if code in item_map]
    selected_prod = st.selectbox("Search for a product:", sorted(valid_descriptions))

    if selected_prod:
        code = desc_to_code[selected_prod]
        
        # Get similarities for the selected product
        if code in similarity.index:
            # Sort similarities and get top 5 (excluding the product itself)
            similar_items = similarity[code].sort_values(ascending=False)[1:6]
            
            st.write(f"### Customers interested in **{selected_prod}** also liked:")
            
            cols = st.columns(5)
            for i, (sim_code, score) in enumerate(similar_items.items()):
                with cols[i]:
                    item_name = item_map.get(sim_code, "Unknown Product")
                    st.success(f"**{item_name}**")
                    st.caption(f"Match Score: {score:.2f}")
        else:
            st.warning("Product code not found in similarity matrix.")
