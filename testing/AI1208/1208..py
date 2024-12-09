import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# 假設我們已經有資料集
data = {
    '行政區': ['松山區', '信義區', '大安區', '中山區', '中正區', '大同區', '萬華區', '文山區', 
              '南港區', '內湖區', '士林區', '北投區'],
    '電動機車數量': [11564, 6271, 6834, 10667, 7538, 4367, 5372, 7531, 3622, 9628, 7967, 7406],
    '現有充電站數量': [15, 13, 15, 15, 9, 9, 10, 10, 9, 17, 18, 13],
    '應有充電站數量': [289, 157, 171, 267, 189, 109, 134, 188, 91, 241, 199, 185]
}

# 將資料轉換為 DataFrame
df = pd.DataFrame(data)

# 計算是否需要增設充電站 (1: 需要增加，0: 不需要)
df['需要增設充電站'] = (df['現有充電站數量'] < df['應有充電站數量']).astype(int)

# 特徵 (X) 和目標變數 (Y)
X = df[['電動機車數量', '現有充電站數量', '應有充電站數量']]
y = df['需要增設充電站']

# 拆分資料集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 初始化邏輯回歸模型
model = LogisticRegression()

# 訓練模型
model.fit(X_train, y_train)

# 預測
y_pred = model.predict(X_test)

# 計算準確率
accuracy = accuracy_score(y_test, y_pred)
print(f'準確率: {accuracy}')

# 顯示混淆矩陣
print(f'混淆矩陣: \n{confusion_matrix(y_test, y_pred)}')

# 顯示模型的係數
print(f'模型係數: {model.coef_}')
