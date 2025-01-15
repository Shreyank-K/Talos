import openai
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.ensemble import GradientBoostingRegressor  # Example ML model
from io import StringIO
from pydantic import BaseModel, ValidationError
import json

class Response(BaseModel):
    total_after_suggestions: str
    allocations: dict  # Keys are categories, values are suggested amounts/details
    risk_score: int
    risks: list  # A list of risk descriptions
    recommendations: list  # A list of actionable recommendations

def generate_analysis(financial_data, goals, industry):
    openai.api_key = "sk-XXXXXXXX"

    prompt = f"""
    Based on the following financial data, business goals, and industry, provide a detailed analysis in JSON format.
    
    Financial Data:
    - Total Money In: ${financial_data['money_in']:,}
    - Total Money Out: ${financial_data['money_out']:,}
    - Current Cash Reserves: ${financial_data['cash_reserves']:,}
    - Current Debt: ${financial_data['debt']:,}
    
    Business Goals:
    {goals}
    
    Industry:
    {industry}
    
    Respond with a JSON object containing:
    - "total_after_suggestions": Total finances after implementing the recommendations.
    - "allocations": A dictionary where keys are categories (e.g., Marketing, Operations, Debt Repayment) and values are suggested amounts or details.
    - "risk_score": An integer between 0-100 indicating the overall financial risk (0 = no risk, 100 = critical risk).
    - "risks": A list of potential risks identified.
    - "recommendations": A list of detailed, actionable recommendations to mitigate risks.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=700,
        temperature=0.7
    )
    
    return response['choices'][0]['text'].strip()

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
st.text_area("ADD SURVEY QUESTIONS HERE")

# Upload Data
st.subheader("Upload Your Financial Data")
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

        # Visualization
        # st.header("Data Visualization")
        # st.subheader("Revenue Trend")
        # if "Revenue" in df.columns:
        #     fig, ax = plt.subplots()
        #     ax.plot(df["Revenue"], label="Revenue Trend")
        #     ax.set_xlabel("Time")
        #     ax.set_ylabel("Revenue")
        #     ax.legend()
        #     st.pyplot(fig)
        # else:
        #     st.warning("No 'revenue' column found in data.")

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
                    financial_data = {
                        "money_in": money_in,
                        "money_out": money_out,
                        "cash_reserves": cash_reserves,
                        "debt": debt
                    }
                    
                    combined_response = generate_analysis(financial_data, goals, industry)
                    
                    try:
                        parsed_response = Response.model_validate_json(combined_response)
                        
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
                        st.text_area("Raw Combined Response", combined_response)

#            st.markdown(f"<div style='border: 1px solid white; padding: 50px; text-align: center;'>{suggestions}</div>", unsafe_allow_html=True)
        
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
