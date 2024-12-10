import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from matplotlib import rcParams

# 設定中文字型
rcParams['font.family'] = ['DFKai-SB']

# 定義每站點支援的電動機車數
bikes_per_station = 125

# 加載數據
sheet3_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\原始資料\sheet3全台縣市電車登記數量原始資料.xlsx'
utf8_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\全台縣市電車登記數量utf8.csv'
station_stats_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\城市與行政區站點統計utf8.csv'

# 1. 預測未來6個月電動機車數量
sheet3_data = pd.read_excel(sheet3_path)
sheet3_data['日期'] = pd.to_datetime(sheet3_data['日期'])
sheet3_data.set_index('日期', inplace=True)
cleaned_data = sheet3_data.replace('-', np.nan).apply(pd.to_numeric, errors='coerce').dropna(axis=0)

future_months = 6
predictions = {}
for column in cleaned_data.columns:
    x = np.arange(len(cleaned_data)).reshape(-1, 1)
    y = cleaned_data[column].values
    model = LinearRegression()
    model.fit(x, y)
    future_x = np.arange(len(cleaned_data), len(cleaned_data) + future_months).reshape(-1, 1)
    predictions[column] = model.predict(future_x)
predictions_df = pd.DataFrame(predictions, index=pd.date_range(cleaned_data.index[-1], periods=future_months + 1, freq='MS')[1:])

# 畫線性回歸圖（以第一個欄位為例）
column_name = cleaned_data.columns[0]
x = np.arange(len(cleaned_data)).reshape(-1, 1)
y = cleaned_data[column_name].values
model = LinearRegression()
model.fit(x, y)
future_y = model.predict(future_x)

plt.figure(figsize=(10, 6))
plt.plot(cleaned_data.index, y, label='歷史數據')
plt.plot(pd.date_range(cleaned_data.index[-1], periods=future_months + 1, freq='MS')[1:], future_y, label='預測數據', linestyle='--')
plt.title(f"線性回歸結果 - {column_name}")
plt.xlabel("日期")
plt.ylabel("數值")
plt.legend()
plt.grid()
plt.show()

# 2. 合併現有數據與站點統計
electric_motorcycles_data = pd.read_csv(utf8_path)
electric_motorcycles_data['縣市'] = electric_motorcycles_data['項目'].str.extract(r'_(\w+市|\w+縣)')
electric_motorcycles_data.rename(columns={"數值": "電動機車數"}, inplace=True)
station_stats_data = pd.read_csv(station_stats_path)

merged_data = pd.merge(electric_motorcycles_data, station_stats_data, on=["縣市", "行政區"], how="inner")
merged_data['應有站點數'] = np.ceil(merged_data['電動機車數'] / bikes_per_station)
merged_data['站點差距'] = merged_data['應有站點數'] - merged_data['站點數量']
merged_data['站點比例'] = merged_data['電動機車數'] / merged_data['站點數量']

# 3. 整合未來預測數據
future_predictions = predictions_df.sum(axis=0)
merged_data['未來電動機車數'] = merged_data['電動機車數'] + merged_data['縣市'].map(future_predictions).fillna(0)
merged_data['未來應有站點數'] = np.ceil(merged_data['未來電動機車數'] / bikes_per_station)
merged_data['未來站點差距'] = merged_data['未來應有站點數'] - merged_data['站點數量']

# 4. 初始化需新增或刪減欄位
merged_data['需新增或刪減'] = 0
merged_data.loc[merged_data['站點差距'] > 0, '需新增或刪減'] = 1
merged_data.loc[merged_data['站點差距'] == 0, '需新增或刪減'] = 2

# 5. 特徵與目標
X = merged_data[['未來電動機車數', '站點數量', '站點比例']]
y = merged_data['需新增或刪減']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. 模型訓練與預測
rf_model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=4)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

# 7. 評估模型
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f"模型準確率: {accuracy}")
print(f"分類報告:\n{report}")

# 畫決策樹圖
plt.figure(figsize=(20, 10))
plot_tree(
    rf_model.estimators_[0],  # 選擇一顆決策樹
    feature_names=X.columns,
    class_names=["不需新增或刪減", "需要新增", "平衡"],
    filled=True,
    fontsize=10
)
plt.title("隨機森林決策樹")
plt.show()

# 8. 保存結果
merged_data['未來預測結果'] = rf_model.predict(X)
output_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\結果\未來站點需求預測.xlsx'
merged_data.to_excel(output_path, index=False)
print(f"結果已保存至: {output_path}")
