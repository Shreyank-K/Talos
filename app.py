import streamlit as st
import requests
from utils import get_analysis, generate_analysis, Response, BACKEND_URL
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the app
st.set_page_config(page_title="Interactive Financial Tool", layout="wide")

# Home Page
st.title("Welcome to the Interactive Financial Tool")
st.markdown("""
    - Upload your financial data to receive tailored insights through AI.
    - Simulate different scenarios and evaluate risks.
    - Gain actionable recommendations for your business.
""")

st.subheader("Quick Survey")
survey_responses = st.text_area("ADD SURVEY QUESTIONS HERE", placeholder="Enter your responses here...")

# Upload Data
st.subheader("Upload Your Financial Data")
uploaded_file = st.file_uploader("Upload CSV/Excel or img", type=["csv", "xlsx", "jpg", "png"])

if uploaded_file:
    try:
        money_in = 100
        money_out = 100
        cash_reserves = 100
        debt = 100
        industry = "e-commerce"

        st.subheader("Goal Input")
        goals = st.text_area("What are your current goals? Ask AI.", placeholder="Increase leads/sales through social media...")
        
        if st.sidebar.button("Generate Analysis"):
            if not goals.strip():
                st.error("Please enter your business goals.")
            else:
                with st.spinner("Processing data..."):
                    response = get_analysis(uploaded_file)
                    if response.status_code == 200:
                        print("yay!")
                        print(response.json())
                    else:
                        print("error!")

                    financial_data = {
                        "money_in": money_in,
                        "money_out": money_out,
                        "cash_reserves": cash_reserves,
                        "debt": debt
                    }
                    
                    try:
                        parsed_response = Response.model_validate_json(response)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.header("Current Finances")
                            st.text_input("Total Before", f"${money_in:,.0f}", disabled=True)
                            st.text_input("Money In", f"${money_in:,.0f}", disabled=True)
                            st.text_input("Money Out", f"${money_out:,.0f}", disabled=True)
                        
                        with col2:
                            st.header("Suggested Allocation")
                            for category, details in parsed_response.allocations.items():
                                st.text_input(category, details, disabled=True)
                            
                            st.text_input("Total After Suggestions", parsed_response.total_after_suggestions, disabled=True)
                        
                        # Display risk analysis
                        st.header("Risk Analysis")
                        st.subheader(f"Risk Score: {parsed_response.risk_score}/100")
                        
                        st.markdown("### Potential Risks")
                        for risk in parsed_response.risks:
                            st.write(f"- {risk}")
                        
                        st.markdown("### Recommendations")
                        for recommendation in parsed_response.recommendations:
                            st.write(f"- {recommendation}")
                    except ValidationError as e:
                        st.error("Failed to parse the API response. Please try again.")
                        st.text_area("Raw Combined Response", response)
        
        def calculate_kpis():
            st.write("Calculation logic goes here.")

        st.markdown(
            """
            <style>
            .center-button {
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }
            .center-button button {
                width: 100px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        clicked = st.button("Calculate", key="calculate_button", help="Click to calculate KPIs", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if clicked:
            calculate_kpis()

        # KPI Section
        st.subheader("Key Performance Indicators")
        for i in range(2):  # Two rows
            cols = st.columns(4)  # Four columns per row
            for col in cols:
                col.markdown("<div style='border: 1px solid white; padding: 20px; text-align: center;'>Current KPIs<br><br>New KPIs</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error("Error reading the file. Please check the format.")
