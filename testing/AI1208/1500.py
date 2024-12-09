import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Step 1: Load the data
station_data = pd.read_csv("Taipei.csv")  # 替換為您的站點數據檔案
registration_data = pd.read_csv("______0____________.csv")  # 替換為您的登記數據檔案

# Step 2: Prepare the data
# Aggregate registration data by district (latest month)
latest_period = registration_data['Statistical Period'].max()
latest_registration = registration_data[registration_data['Statistical Period'] == latest_period]
latest_registration = latest_registration.iloc[:, 1:]  # Exclude the time period column

# Summarize total registrations by district
district_totals = latest_registration.sum().reset_index()
district_totals.columns = ['District', 'Registration Count']

# Merge district totals with existing station data
station_data['dist'] = station_data['dist'].str.strip()
district_totals['District'] = district_totals['District'].str.replace('_新增數量', '').str.strip()
merged_data = pd.merge(station_data, district_totals, left_on='dist', right_on='District', how='inner')

# Feature: Registration count, Coordinates (lat/lon)
X = merged_data[['Registration Count', 'lat', 'lon']]

# Target: Binary classification - whether a district needs a new station
motorcycles_per_station = 40
merged_data['Required Stations'] = (merged_data['Registration Count'] / motorcycles_per_station).apply(lambda x: int(x) + 1)
merged_data['Needs Station'] = (merged_data['Required Stations'] > merged_data.groupby('dist')['dist'].transform('size')).astype(int)

y = merged_data['Needs Station']

# Step 3: Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 4: Train logistic regression model
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = log_reg.predict(X_test)

# Step 6: Evaluate model
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
