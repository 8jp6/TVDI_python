#env Forml(L)
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 載入數據集（以鸢尾花數據集為例）
iris = datasets.load_iris()
X = iris.data  # 特徵
y = iris.target  # 標籤

# 切分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 創建 KNN 分類器
knn = KNeighborsClassifier(n_neighbors=3)

# 在訓練集上訓練模型
knn.fit(X_train, y_train)

# 在測試集上進行預測
y_pred = knn.predict(X_test)

# 計算準確率
accuracy = accuracy_score(y_test, y_pred)
print(f'準確率: {accuracy:.2f}')
