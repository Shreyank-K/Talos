import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.ensemble import GradientBoostingRegressor  # Example ML model
from io import StringIO

# Initialize the app
st.set_page_config(page_title="Interactive Financial Tool", layout="wide")

# Sidebar navigation
menu = ["Home", "Upload Data", "Visualization", "Risk Analysis", "Insights", "About"]
choice = st.sidebar.selectbox("Navigation", menu)

# Home Page
if choice == "Home":
    st.title("Welcome to the Interactive Financial Tool")
    st.markdown("""
        - Upload your financial data to receive tailored insights.
        - Simulate different scenarios and evaluate risks.
        - Gain actionable recommendations for your business.
    """)

# Upload Data
elif choice == "Upload Data":
    st.header("Upload Your Financial Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("File Uploaded Successfully!")
            st.write("Preview of Uploaded Data:")
            st.dataframe(df.head())
        except Exception as e:
            st.error("Error reading the file. Please check the format.")

# Visualization
elif choice == "Visualization":
    st.header("Data Visualization")
    st.markdown("Upload your data to see visualizations.")
    if 'df' in locals():
        st.subheader("Revenue Trend")
        if "revenue" in df.columns:
            fig, ax = plt.subplots()
            ax.plot(df["revenue"], label="Revenue Trend")
            ax.set_xlabel("Time")
            ax.set_ylabel("Revenue")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("No 'revenue' column found in data.")
    else:
        st.warning("Please upload data first.")

# Risk Analysis
elif choice == "Risk Analysis":
    st.header("Risk Analysis")
    st.markdown("Perform sensitivity analysis to evaluate potential risks.")
    st.slider("Adjust variable sensitivity", 0, 100, 50)

# Insights
elif choice == "Insights":
    st.header("AI-Generated Insights")
    st.text_area("Enter financial questions or documents for analysis.")
    if st.button("Generate Insights"):
        st.success("This is where GPT-generated insights would appear.")

# About
elif choice == "About":
    st.header("About the Tool")
    st.markdown("""
        This tool uses a hybrid AI approach combining Machine Learning and GPT to provide actionable financial insights for small businesses.
        """)
    st.info("For feedback or questions, use the form in the sidebar.")
