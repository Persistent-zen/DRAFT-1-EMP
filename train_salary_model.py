import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the dataset
df = pd.read_csv('employee_dataset.csv')

# Define features and target
X = df.drop('Salary', axis=1)
y = df['Salary']

# Categorical and numeric columns
categorical_cols = ['Education Level', 'Role', 'Department', 'Location']
numeric_cols = ['Age', 'Years of Experience']

# Preprocessing: OneHotEncode categoricals, passthrough numerics
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ('num', 'passthrough', numeric_cols)
    ]
)

# Build the pipeline with preprocessor + model
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(X_train, y_train)

# Evaluate
y_pred = model_pipeline.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Model Evaluation:")
print(f" - RMSE: {rmse:.2f}")
print(f" - R2 Score: {r2:.2f}")

# Save the trained pipeline (includes preprocessing + model)
joblib.dump(model_pipeline, 'salary_predictor.pkl')
print("Trained model saved as 'salary_predictor.pkl'")
