import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
from sklearn.tree import export_text

# 定義每站點支援的電動機車數
bikes_per_station = 125



# 載入資料
file_path_vehicle = r'C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\全台縣市電車登記數量utf8.csv'
file_path_station = r'C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\城市與行政區站點統計utf8.csv'
electric_motorcycles_data = pd.read_csv(file_path_vehicle)
station_stats_data = pd.read_csv(file_path_station)

# 提取縣市資訊
electric_motorcycles_data['縣市'] = electric_motorcycles_data['項目'].str.extract(r'_(\w+市|\w+縣)')
electric_motorcycles_data.rename(columns={"數值": "電動機車數"}, inplace=True)

# 合併資料
merged_data = pd.merge(
    electric_motorcycles_data,
    station_stats_data,
    on=["縣市", "行政區"],
    how="inner"
)

# 計算應有站點數與站點比例
merged_data['應有站點數'] = np.ceil(merged_data['電動機車數'] / bikes_per_station)
merged_data['站點比例'] = merged_data['電動機車數'] / merged_data['站點數量']

# 站點比例應該是電車總數除以應有站點數這樣才知道皆不接近1:125
merged_data['站點差距'] = merged_data['應有站點數'] - merged_data['站點數量']

# 根據站點差距設置需新增或刪減值
merged_data['需新增或刪減'] = 0  # 預設為不需要新增或刪減
merged_data.loc[merged_data['站點差距'] > 0, '需新增或刪減'] = 1  # 需要新增
merged_data.loc[merged_data['站點差距'] == 0, '需新增或刪減'] = 2  # 現有站點數與應有站點數相同

# 準備特徵與目標
X = merged_data[['電動機車數', '站點數量', '站點比例']]  # 特徵
y = merged_data['需新增或刪減']  # 目標

# 分割訓練與測試數據
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
max_depth = 4

# 訓練隨機森林模型
rf_model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=max_depth)
rf_model.fit(X_train, y_train)

# 評估模型
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Random Forest Model Accuracy:", accuracy)
print("\nClassification Report:\n", report)

# 將預測結果添加到資料集中
merged_data['預測結果'] = rf_model.predict(X)
merged_data.loc[merged_data['站點差距'] == 0, '預測結果'] = 2  # 更新預測結果，當站點數相同時為 2

# 保存結果為 Excel 檔案
# output_file = r'C:\Users\ASUS\Desktop\GItHub\TVDI_python\testing\AI\第二階段預測增多少_結果.xlsx'
# merged_data.to_excel(output_file, index=False)
# print(f"預測結果已保存到 {output_file}")

# 繪製隨機森林中的一顆決策樹
plt.figure(figsize=(20, 10))
plot_tree(
    rf_model.estimators_[0],  # 隨機選取一顆決策樹
    feature_names=X.columns,
    class_names=["No Add/Delete", "Add/Delete", "Balanced"],
    filled=True,
    fontsize=10
)
plt.title("Visualization of a Decision Tree in Random Forest")
plt.show()