import pandas as pd
import numpy as np
import random

# Sample data pools
education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
roles = ['Data Scientist', 'Software Engineer', 'Data Analyst', 'Manager', 'Consultant',
         'Product Manager', 'System Administrator', 'QA Engineer', 'Business Analyst']
departments = ['IT', 'HR', 'Finance', 'Marketing', 'Operations', 'Product', 'Customer Support']
locations = ['New York', 'San Francisco', 'Austin', 'Seattle', 'Chicago', 'Boston', 'Los Angeles']

# Function to generate salary based on features
def calculate_salary(experience, education, role, department, location, age):
    base = 30000 + (experience * 1800)
    education_bonus = {'High School': 0, 'Associate': 5000, 'Bachelor': 10000, 'Master': 20000, 'PhD': 35000}
    role_multiplier = {
        'Data Scientist': 1.4, 'Software Engineer': 1.3, 'Data Analyst': 1.15, 'Manager': 1.45,
        'Consultant': 1.25, 'Product Manager': 1.5, 'System Administrator': 1.1,
        'QA Engineer': 1.1, 'Business Analyst': 1.2
    }
    city_cost = {
        'New York': 1.4, 'San Francisco': 1.5, 'Austin': 1.1, 'Seattle': 1.3,
        'Chicago': 1.2, 'Boston': 1.35, 'Los Angeles': 1.4
    }
    
    salary = base
    salary += education_bonus.get(education, 0)
    salary *= role_multiplier.get(role, 1.0)
    salary *= city_cost.get(location, 1.0)
    salary += (age - 22) * 450  # age premium

    # Add random noise for realism
    noise = np.random.normal(0, 5000)
    salary += noise

    return round(max(salary, 20000), 2)  # Prevent absurdly low salaries

# Generate synthetic data
num_samples = 10000
data = []

for _ in range(num_samples):
    age = random.randint(22, 60)
    education = random.choice(education_levels)
    experience = random.randint(0, age - 22)
    role = random.choice(roles)
    department = random.choice(departments)
    location = random.choice(locations)
    salary = calculate_salary(experience, education, role, department, location, age)

    data.append([age, education, experience, role, department, location, salary])

# Create DataFrame
columns = ['Age', 'Education Level', 'Years of Experience', 'Role', 'Department', 'Location', 'Salary']
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('employee_dataset.csv', index=False)
print(f"Synthetic dataset with {num_samples} samples generated and saved as 'employee_dataset.csv'")
