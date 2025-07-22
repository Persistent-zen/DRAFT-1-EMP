import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load the cleaned salary dataset
df = pd.read_csv('data/cleaned_data.csv')

# Define feature columns and target
features = ['Experience Level', 'Employment Type', 'Job Title',
            'Employee Residence', 'Company Location', 'Company Size']
target = 'Salary'

# Encode categorical features
label_encoders = {}
for feature in features:
    le = LabelEncoder()
    df[feature] = le.fit_transform(df[feature])
    label_encoders[feature] = le

# Split data
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Evaluation on Real Data:")
print(f" - RMSE: {rmse:.2f}")
print(f" - MAE: {mae:.2f}")
print(f" - R² Score: {r2:.2f}")

# Save model and encoders
joblib.dump(model, 'real_salary_predictor.pkl')
joblib.dump(label_encoders, 'real_salary_label_encoders.pkl')

print("Trained model saved as 'real_salary_predictor.pkl'")
print("Label encoders saved as 'real_salary_label_encoders.pkl'")
