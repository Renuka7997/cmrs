import os
import sys
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import joblib

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

#dataset
data = pd.read_csv("C:\\Users\\RENUKA\\OneDrive\\Desktop\\Construction Material Recommendation System\\cmrs_dataset.csv")

print(data.head())

# Encoding
categorical_columns = ['Building_type', 'Property_type', 'Climate_type', 'Soil_type', 'Budget', 'Category', 'Location']
label_encoders = {}

for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le
    joblib.dump(le, f'{col}_encoder.pkl')

#target split
X = data.drop('Recommended_material', axis=1)
y = data['Recommended_material']

# Scale and save
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, 'scaler.pkl')

# Handled imbalance
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X_scaled, y)


X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, 'random_forest.pkl')

y_pred = model.predict(X_test)
print(f"Classification Report:\n{classification_report(y_test, y_pred, zero_division=0)}")
