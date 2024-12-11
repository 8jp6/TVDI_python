import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import cross_val_score   

# Set font to support Chinese characters
matplotlib.rc("font", family="Microsoft JhengHei")

# Load the data
file_path = r"C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\proj_proj\202410合併數據.xlsx"
data = pd.read_excel(file_path)

# Define classify function
def classify(row):
    ratio = row['電車登記數'] / row['站點小計'] if row['站點小計'] > 0 else 0
    if ratio < 95:
        return '減少'
    elif ratio > 155:
        return '新增'
    else:
        return '保持不變'

# Add a new column for the target variable
data['決策'] = data.apply(classify, axis=1)

data['比例偏離度'] = abs((data['電車登記數'] / (data['站點小計'].replace(0, 1))) - 125)

# Select features and target
features = ['2024人口數', '土地面積', '人口密度/平方公里', '電車登記數', '站點小計', '比例偏離度']
target = '決策'
X = data[features]
y = data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train a Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42,max_depth=3,n_estimators=1000,max_features=5)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
report = classification_report(y_test, y_pred, target_names=label_map.keys())
scores = cross_val_score(rf_model, X, y, cv=5)  # 5-fold cross-validation
accuracy = accuracy_score(y_test, y_pred)
importances = rf_model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"特徵: {feature}, 重要性: {importance:.2f}")

print(f'平均準確度: {scores.mean():.2f}')
print(f"模型準確率: {accuracy}")
print(report)


# Visualize one of the trees in the forest
plt.figure(figsize=(20, 10))
plot_tree(rf_model.estimators_[0], 
          feature_names=features, 
          class_names=list(label_map.keys()), 
          filled=True, 
          rounded=True)
plt.title("森林中的一棵樹", fontsize=16)
plt.show()

