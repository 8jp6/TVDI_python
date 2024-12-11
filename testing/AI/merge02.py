import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from matplotlib import rcParams
from sklearn.preprocessing import PolynomialFeatures

# 設定中文字型
rcParams['font.family'] = ['DFKai-SB']

# 定義每站點支援的電動機車數
bikes_per_station = 125

# 加載數據
sheet3_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\原始資料\sheet3全台縣市電車登記數量原始資料.xlsx'
utf8_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\全台縣市電車登記數量utf8.csv'
station_stats_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\城市與行政區站點統計utf8.csv'

# 1. 預測未來6個月電動機車數量（線性回歸部分）
sheet3_data = pd.read_excel(sheet3_path)
sheet3_data['日期'] = pd.to_datetime(sheet3_data['日期'])
sheet3_data.set_index('日期', inplace=True)

# 清理數據
numeric_columns = sheet3_data.select_dtypes(include=[np.number]).columns
sheet3_data_cleaned = sheet3_data[numeric_columns].replace('-', np.nan)
sheet3_data_cleaned = sheet3_data_cleaned.apply(pd.to_numeric, errors='coerce').fillna(sheet3_data_cleaned.mean())

# 預測未來數據
future_months = 6

# Using Polynomial Regression (degree 2)
predictions_poly = {}
poly = PolynomialFeatures(degree=2)
predictions_pr = {}

for column in sheet3_data_cleaned.columns:
    x_pr = np.arange(len(sheet3_data_cleaned)).reshape(-1, 1)
    y_pr = sheet3_data_cleaned[column].values
    model_pr = LinearRegression()
    model_pr.fit(x_pr, y_pr)
    future_x_pr = np.arange(len(sheet3_data_cleaned), len(sheet3_data_cleaned) + future_months).reshape(-1, 1)
    predictions_pr[column] = model_pr.predict(future_x_pr)
    x_poly = poly.fit_transform(x_pr)
    y_pr = sheet3_data_cleaned[column].values
    model_poly = LinearRegression()
    model_poly.fit(x_poly, y_pr)
    future_x_poly = poly.transform(future_x_pr)
    predictions_poly[column] = model_poly.predict(future_x_poly)

predictions_df_poly = pd.DataFrame(predictions_poly, index=pd.date_range(sheet3_data_cleaned.index[-1], periods=future_months + 1, freq='MS')[1:])
future_predictions_dict_fixed = {str(k): v for k, v in predictions_df_poly.iloc[-1].to_dict().items()}

# Plotting for the first column
column_name = sheet3_data_cleaned.columns[0]
x_poly = poly.fit_transform(x_pr)
y = sheet3_data_cleaned[column_name].values
model_poly = LinearRegression()
model_poly.fit(x_poly, y)
future_y_poly = model_poly.predict(future_x_poly)

plt.figure(figsize=(10, 6))
# Plot historical data
plt.plot(sheet3_data_cleaned.index, y, label='歷史數據', color='blue')

# Plot predictions separately
plt.plot(pd.date_range(sheet3_data_cleaned.index[-1], periods=future_months + 1, freq='MS')[1:], future_y_poly, label='預測數據', color='orange')

# Connect the historical and prediction data
plt.plot(
    np.concatenate([sheet3_data_cleaned.index, pd.date_range(sheet3_data_cleaned.index[-1], periods=future_months + 1, freq='MS')[1:]]),
    np.concatenate([y, future_y_poly]),
    color='gray', linestyle=':'  # Use a subtle line to indicate connection
)

plt.title(f"多項式回歸 (2次) 結果 - {column_name}")
plt.xlabel("日期")
plt.ylabel("數值")
plt.legend()
plt.grid()
plt.show()

# 2. 合併現有數據與站點統計（隨機森林部分）
electric_motorcycles_data = pd.read_csv(utf8_path)
station_stats_data = pd.read_csv(station_stats_path)

electric_motorcycles_data['縣市'] = electric_motorcycles_data['項目'].str.extract(r'_(\w+市|\w+縣)')
electric_motorcycles_data.rename(columns={"數值": "電動機車數"}, inplace=True)

merged_data = pd.merge(electric_motorcycles_data, station_stats_data, on=["縣市", "行政區"], how="inner")

# 定義每站點支援的電動機車數
bikes_per_station = 125

# 計算站點需求數據
merged_data['未來電動機車數'] = merged_data['未來電動機車數'] = merged_data['項目'].apply(
    lambda x: future_predictions_dict_fixed.get(str(x), 0))
merged_data['未來應有站點數'] = np.ceil(merged_data['未來電動機車數'] / bikes_per_station)
merged_data['站點比例'] = merged_data['未來電動機車數'] / merged_data['未來應有站點數']
merged_data['未來站點差距'] = merged_data['未來應有站點數'] - merged_data['站點數量']
merged_data['需新增或刪減'] = 0
merged_data.loc[merged_data['未來站點差距'] > 0, '需新增或刪減'] = 1
merged_data.loc[merged_data['未來站點差距'] == 0, '需新增或刪減'] = 2

# 隨機森林模型
X = merged_data[['未來電動機車數', '站點數量', '站點比例']]
y = merged_data['需新增或刪減']

# 分割訓練與測試數據
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 訓練隨機森林模型
rf_model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=3)
rf_model.fit(X_train, y_train)

# 評估模型
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f"模型準確率: {accuracy}")
print(f"分類報告:\n{report}")

# 繪製隨機森林中的一顆決策樹
plt.figure(figsize=(20, 10))
plot_tree(rf_model.estimators_[0], feature_names=X.columns, class_names=["不需新增或刪減", "需要新增", "平衡"], filled=True, fontsize=10)
plt.title("隨機森林決策樹")
plt.show()

print(merged_data[merged_data['縣市'] == '臺北市'])

# 保存結果
output_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\第三階段預測車輛數再預測增減_結果.xlsx'
merged_data.to_excel(output_path, index=False)
print(f"結果已保存至: {output_path}")
