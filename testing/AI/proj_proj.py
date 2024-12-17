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
file_path = r"C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\202410合併數據.xlsx"
data = pd.read_excel(file_path)

# Add a new column for the target variable ('新增', '減少', '保持不變')
def classify(row):
    ratio = row['電車登記數'] / row['站點小計'] if row['站點小計'] > 0 else 0
    if ratio < 95:  # 125 - 30 = 95
        return '減少'
    elif ratio > 155:  # 125 + 30 = 155
        return '新增'
    else:
        return '保持不變'

data['決策'] = data.apply(classify, axis=1)

# Encode the target variable
label_map = {'新增': 0, '保持不變': 1, '減少': 2}
data['決策編碼'] = data['決策'].map(label_map)

# Select features and target
features = ['2024人口數', '土地面積', '人口密度/平方公里','電車登記數', '站點小計']
target = '決策編碼'
X = data[features]
y = data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train a Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42,max_depth=3,n_estimators=1000,max_features=5)
rf_model.fit(X_train, y_train)


def get_model_metrics(rf_model, X, y, label_map):
    """
    計算模型的分類報告和相關數據。
    """
    # Make predictions
    y_pred = rf_model.predict(X_test)

    # Evaluate the model
    report = classification_report(y_test, y_pred, target_names=label_map.keys(),output_dict=True)
    report["accuracy"] = {
    "precision": None,
    "recall": None,
    "f1-score": report["accuracy"],
    "support": report["macro avg"]["support"]  # 或 weighted avg 的 support
    }
    scores = cross_val_score(rf_model, X, y, cv=5)  # 5-fold cross-validation
    accuracy = accuracy_score(y_test, y_pred)
    print(f'平均準確度: {scores.mean():.2f}')
    print(f"模型準確率: {accuracy}")
    print(report)
    return report, scores, accuracy




# Visualize one of the trees in the forest
def draw_decision_tree(model, features, class_names, figsize=(10, 5), fullscreen=True):
    fig = plt.figure(figsize=figsize)
    plot_tree(
        model.estimators_[0],
        feature_names=features,
        class_names=class_names,
        filled=True,
        rounded=True
    )
    plt.title("森林中的一棵樹", fontsize=16)

    # 如果启用了全屏
    if fullscreen:
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')  # 窗口最大化

    return fig

def load_data():
        # 加载数据
    data = pd.read_excel(r'C:\Users\user\Desktop\程式在這裡\GitHub\TVDI_python\testing\AI\202410合併數據.xlsx')
    counties = data['縣市'].drop_duplicates().tolist()
    regions = data.groupby('縣市')['區域別'].apply(list).to_dict()
    return data, counties, regions


# if __name__ == '__main__':
#     draw_decision_tree(rf_model, features, list(label_map.keys()))