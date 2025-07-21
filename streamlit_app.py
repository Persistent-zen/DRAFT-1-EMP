import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Employee Salary Predictor & Savings Estimator")

# ---- Input Fields ----
st.header("Enter Employee Details")
experience = st.number_input('Years of Experience', min_value=0.0, max_value=50.0, step=0.5)
education = st.selectbox('Education Level', ['High School', 'Bachelor', 'Master', 'PhD'])
age = st.number_input('Age', min_value=18, max_value=70)
role = st.text_input('Job Role')
department = st.text_input('Department')

# ---- Dummy Salary Prediction ----
if st.button('Predict Salary'):
    base_salary = 30000 + (experience * 1500)
    education_bonus = {'High School': 0, 'Bachelor': 5000, 'Master': 10000, 'PhD': 20000}
    predicted_salary = base_salary + education_bonus.get(education, 0)
    
    st.success(f'Estimated Gross Salary: ${predicted_salary:,.2f}')
    
    # Savings Estimator
    st.header("💰 Savings Estimator")
    savings_rate = st.slider('What % of your salary do you want to save?', 0, 50, 20)
    monthly_savings = (predicted_salary / 12) * (savings_rate / 100)
    st.info(f'You can save approximately **${monthly_savings:,.2f} per month** at a {savings_rate}% savings rate.')

    # Visualization
    st.subheader("Projected Savings Over 1 Year")
    months = np.arange(1, 13)
    savings_projection = months * monthly_savings
    
    fig, ax = plt.subplots()
    ax.plot(months, savings_projection, marker='o')
    ax.set_xlabel('Month')
    ax.set_ylabel('Cumulative Savings ($)')
    ax.set_title('1-Year Savings Projection')
    st.pyplot(fig)
