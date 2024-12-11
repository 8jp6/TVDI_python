import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 讀取 Excel 檔案
file_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\原始資料\sheet3全台縣市電車登記數量原始資料.xlsx'
sheet3_data = pd.read_excel(file_path)



# 日期處理
sheet3_data['日期'] = pd.to_datetime(sheet3_data['日期'])
sheet3_data.set_index('日期', inplace=True)

# 數據清洗：替換非數字值並處理缺失值
cleaned_data = sheet3_data.replace(to_replace='-', value=np.nan)
cleaned_data = cleaned_data.apply(pd.to_numeric, errors='coerce')
threshold = 0.5 * len(cleaned_data)
cleaned_data = cleaned_data.dropna(axis=1, thresh=threshold)
cleaned_data = cleaned_data.fillna(cleaned_data.mean())

# 預測每個欄位未來新增數量
future_months = 6
predictions = {}

for column in cleaned_data.columns:
    # 準備數據
    x = np.arange(len(cleaned_data)).reshape(-1, 1)
    y = cleaned_data[column].values
    
    # 建立並訓練模型
    model = LinearRegression()
    model.fit(x, y)
    
    # 預測未來新增數量
    future_x = np.arange(len(cleaned_data), len(cleaned_data) + future_months).reshape(-1, 1)
    predictions[column] = model.predict(future_x)

# 將預測結果轉為 DataFrame
predictions_df = pd.DataFrame(predictions, index=pd.date_range(cleaned_data.index[-1], periods=future_months + 1, freq='MS')[1:])

# 輸出結果
print("每欄未來新增數量預測：")
print(predictions_df)

# 如果需要存檔
# output_file_path = r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\每欄未來新增數量預測.xlsx'
# predictions_df.to_excel(output_file_path)