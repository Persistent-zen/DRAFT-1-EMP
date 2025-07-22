import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# --- Config ---
st.set_page_config(page_title="Employee Salary Prediction", page_icon="💼", layout="centered")

model = joblib.load('real_salary_predictor.pkl')
df = pd.read_csv('data/cleaned_data.csv')

USD_TO_INR = 83  # USD to INR conversion rate

st.title("💼 Employee Salary Prediction")

st.markdown("""
Welcome to the Employee Salary & Savings Estimator! 
Predict your annual salary based on your professional profile, compare it with the industry average, 
adjust for cost of living, and estimate potential savings.
""")

st.divider()
st.header("👤 Enter Your Professional Details")

experience_level = st.selectbox('Experience Level', ['Entry-Level', 'Mid-Level', 'Senior-Level', 'Executive'])
employment_type = st.selectbox('Employment Type', ['Full-Time', 'Part-Time', 'Contract', 'Freelance'])

# Job Title input
common_job_titles = ['Data Scientist', 'Software Engineer', 'Machine Learning Engineer', 'Product Manager',
                     'Data Analyst', 'AI Researcher', 'Business Analyst', 'DevOps Engineer', 'Cloud Architect', 'Other']
dataset_job_titles = df['Job Title'].unique().tolist()
all_job_titles = sorted(list(set(common_job_titles + dataset_job_titles + ['Other'])))

selected_job_title = st.selectbox('Job Title', all_job_titles)
job_title = st.text_input('Enter your Job Title') if selected_job_title == 'Other' else selected_job_title

# Country of Residence input
common_countries = ['United States', 'India', 'United Kingdom', 'Canada', 'Germany',
                    'Australia', 'France', 'Japan', 'Singapore', 'Brazil', 'Other']
dataset_countries = df['Employee Residence'].unique().tolist()
all_countries = sorted(list(set(common_countries + dataset_countries + ['Other'])))

selected_country = st.selectbox('Country of Residence', all_countries)
employee_residence = st.text_input('Enter your Country of Residence') if selected_country == 'Other' else selected_country

# Company Headquarters Location input
dataset_company_locations = df['Company Location'].unique().tolist()
all_company_locations = sorted(list(set(common_countries + dataset_company_locations + ['Other'])))

selected_company_location = st.selectbox('Company Headquarters Location', all_company_locations)
company_location = st.text_input('Enter Company Headquarters Location') if selected_company_location == 'Other' else selected_company_location

company_size = st.selectbox('Company Size', ['Small (1-50 employees)', 'Medium (51-250 employees)', 'Large (251+ employees)'])

# Initialize session state for salary
if 'predicted_salary' not in st.session_state:
    st.session_state.predicted_salary = None

if st.button('🔎 Predict My Salary'):
    experience_map = {'Entry-Level': 'EN', 'Mid-Level': 'MI', 'Senior-Level': 'SE', 'Executive': 'EX'}
    employment_map = {'Full-Time': 'FT', 'Part-Time': 'PT', 'Contract': 'CT', 'Freelance': 'FL'}
    company_size_map = {'Small (1-50 employees)': 'S', 'Medium (51-250 employees)': 'M', 'Large (251+ employees)': 'L'}

    input_data = pd.DataFrame([{
        'Experience Level': experience_map[experience_level],
        'Employment Type': employment_map[employment_type],
        'Job Title': job_title,
        'Employee Residence': employee_residence,
        'Company Location': company_location,
        'Company Size': company_size_map[company_size]
    }])

    predicted_salary = model.predict(input_data)[0]
    st.session_state.predicted_salary = predicted_salary

if st.session_state.predicted_salary:
    predicted_salary = st.session_state.predicted_salary
    st.success(f"🎯 Predicted Annual Salary: **${predicted_salary:,.2f} USD / ₹{predicted_salary * USD_TO_INR:,.2f} INR**")

    st.divider()
    st.subheader("📊 Industry Salary Benchmark")

    average_salary = df[df['Job Title'].str.lower() == job_title.lower()]['Salary'].mean()

    if not np.isnan(average_salary):
        st.info(f"Average salary for **{job_title.title()}**: **${average_salary:,.2f} USD / ₹{average_salary * USD_TO_INR:,.2f} INR**")
    else:
        st.info("⚠️ Industry average salary data for this job title is not available in our dataset.")
        search_query = job_title.replace(' ', '+') + '+average+salary'
        google_search_url = f"https://www.google.com/search?q={search_query}"
        glassdoor_url = f"https://www.glassdoor.com/Salaries/{job_title.replace(' ', '-')}-salary-SRCH_KO0,{len(job_title)}.htm"
        st.markdown(f"[🔎 Search '{job_title} average salary' on Google]({google_search_url})", unsafe_allow_html=True)
        st.markdown(f"[🟩 View '{job_title}' salaries on Glassdoor]({glassdoor_url})", unsafe_allow_html=True)

    st.divider()
    st.subheader("🌍 Cost of Living Adjustment")

    cost_of_living_index = {
        'United States': 100, 'India': 30, 'United Kingdom': 85, 'Germany': 75, 'Australia': 90, 'Canada': 80,
        'France': 78, 'Japan': 82, 'Singapore': 95, 'Brazil': 40, 'South Africa': 35, 'China': 50,
        'United Arab Emirates': 70, 'Switzerland': 120, 'Netherlands': 88, 'Sweden': 84, 'Spain': 70, 'Italy': 68
    }

    user_country = employee_residence.title().strip()
    user_col_index = cost_of_living_index.get(user_country, 100)

    st.info(f"📌 Average Cost of Living Index for **{user_country}**: **{user_col_index}** (Base = 100 for USA)")

    adjusted_salary = predicted_salary * (100 / user_col_index)
    st.success(f"Your salary adjusted for cost of living in **{user_country}**: "
               f"**${adjusted_salary:,.2f} USD / ₹{adjusted_salary * USD_TO_INR:,.2f} INR**")

    if st.checkbox('Show Cost of Living Index for All Countries'):
        col_df = pd.DataFrame(list(cost_of_living_index.items()), columns=['Country', 'Cost of Living Index']).sort_values('Cost of Living Index', ascending=False)
        st.table(col_df.reset_index(drop=True))

    st.divider()
    st.header("💰 Monthly Savings Estimator")

    savings_rate = st.slider('What percentage of your salary would you like to save monthly?', 0, 50, 20)
    monthly_savings = (predicted_salary / 12) * (savings_rate / 100)

    st.info(f"At a {savings_rate}% savings rate, you can save approximately **${monthly_savings:,.2f} per month / ₹{monthly_savings * USD_TO_INR:,.2f} INR per month**.")

    st.subheader("📈 Projected Cumulative Savings Over 1 Year")
    months = np.arange(1, 13)
    savings_projection = months * monthly_savings

    fig, ax = plt.subplots()
    ax.plot(months, savings_projection, marker='o', color='green')
    ax.set_xlabel('Month')
    ax.set_ylabel('Cumulative Savings (USD)')
    ax.set_title('1-Year Savings Projection')
    st.pyplot(fig)
