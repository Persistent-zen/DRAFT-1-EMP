import pandas as pd

# Load your dataset
df = pd.read_csv('ds_salaries.csv')   # <-- use exact filename here

print("Initial Data Preview:")
print(df.head())
print("\nColumns:\n", df.columns)

# Drop unnecessary columns (adjust for this dataset)
columns_to_keep = [
    'experience_level', 'employment_type', 'job_title', 'salary_in_usd',
    'employee_residence', 'company_location', 'company_size'
]
df = df[columns_to_keep]

# Rename columns for consistency
df.rename(columns={
    'experience_level': 'Experience Level',
    'employment_type': 'Employment Type',
    'job_title': 'Job Title',
    'salary_in_usd': 'Salary',
    'employee_residence': 'Employee Residence',
    'company_location': 'Company Location',
    'company_size': 'Company Size'
}, inplace=True)

# Check for missing values
print("\nMissing Values:\n", df.isnull().sum())

# Drop rows with missing salaries
df.dropna(subset=['Salary'], inplace=True)

print("\nCleaned Data Preview:")
print(df.head())

# Save cleaned data
df.to_csv('cleaned_data.csv', index=False)
print("\nCleaned dataset saved as 'cleaned_data.csv'")
