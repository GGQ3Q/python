import numpy as np
import pandas as pd


# 1 数据加载与基础工具函数


# 数据集划分
def train_test_split_custom(X, y, test_size=0.2, random_state=42):
    np.random.seed(random_state)
    shuffled_indices = np.random.permutation(len(X))
    test_set_size = int(len(X) * test_size)

    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]


# 标准化 (Z-score Normalization)
def standardize(X_train, X_test):
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)
    std[std == 0] = 1e-8  # 防止除零错误

    X_train_scaled = (X_train - mean) / std
    X_test_scaled = (X_test - mean) / std
    return X_train_scaled, X_test_scaled


# 2. 线性回归模型 (预测连续分数)

class CustomLinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 梯度下降
        for _ in range(self.epochs):
            y_pred = np.dot(X, self.weights) + self.bias

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            # 更新参数
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias



# 3. 逻辑回归模型 (预测二分类：好酒/坏酒)

class CustomLogisticRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def _sigmoid(self, z):
        # 限制z的范围防止exp溢出
        z = np.clip(z, -250, 250)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 梯度下降
        for _ in range(self.epochs):
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(linear_model)

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            # 更新参数
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        return self._sigmoid(linear_model)

    def predict(self, X, threshold=0.5):
        y_pred_proba = self.predict_proba(X)
        return (y_pred_proba >= threshold).astype(int)



# 4. 主程序运行与模型评估

if __name__ == "__main__":
    # 假设数据集已下载到本地，路径为 'winequality-red.csv'
    # 分隔符通常是分号 ';'
    try:
        df = pd.read_csv('winequality-red.csv', sep=';')
    except FileNotFoundError:
        print("请确保 'winequality-red.csv' 文件在当前目录下。")
        exit()

    X = df.drop('quality', axis=1).values
    y_reg = df['quality'].values  # 回归标签
    y_clf = (y_reg > 6).astype(int)  # 分类标签 (质量 > 6 为好酒)

    # 划分与标准化数据
    X_train, X_test, y_reg_train, y_reg_test = train_test_split_custom(X, y_reg)
    _, _, y_clf_train, y_clf_test = train_test_split_custom(X, y_clf)

    X_train_scaled, X_test_scaled = standardize(X_train, X_test)

    # --- 任务 1: 线性回归 ---
    lin_reg = CustomLinearRegression(learning_rate=0.1, epochs=2000)
    lin_reg.fit(X_train_scaled, y_reg_train)
    reg_predictions = lin_reg.predict(X_test_scaled)

    mse = np.mean((reg_predictions - y_reg_test) ** 2)
    print("--- 线性回归模型评估 ---")
    print(f"均方误差 (MSE): {mse:.4f}")

    # 任务 2: 逻辑回归
    log_reg = CustomLogisticRegression(learning_rate=0.1, epochs=2000)
    log_reg.fit(X_train_scaled, y_clf_train)
    clf_predictions = log_reg.predict(X_test_scaled)

    # 计算分类指标
    tp = np.sum((clf_predictions == 1) & (y_clf_test == 1))
    tn = np.sum((clf_predictions == 0) & (y_clf_test == 0))
    fp = np.sum((clf_predictions == 1) & (y_clf_test == 0))
    fn = np.sum((clf_predictions == 0) & (y_clf_test == 1))

    accuracy = (tp + tn) / len(y_clf_test)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    print("\n--- 逻辑回归模型评估 ---")
    print(f"准确率 (Accuracy): {accuracy:.4f}")
    print(f"精确率 (Precision): {precision:.4f}")
    print(f"召回率 (Recall): {recall:.4f}")
