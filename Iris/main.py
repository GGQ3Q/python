import numpy as np
import pandas as pd



# 1. K-Means 模型实现

class CustomKMeans:
    def __init__(self, k=3, max_iters=100, random_state=42):
        self.k = k
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = None
        self.labels = None
        self.inertia = 0  # WCSS (簇内误差平方和)

    def _euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def fit(self, X):
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        # 1. 随机初始化聚类中心 (从数据集中随机挑k个点)
        random_indices = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[random_indices]

        for _ in range(self.max_iters):
            # 2. 分配簇
            self.labels = self._create_clusters(X)

            # 保存旧的中心用于判断是否收敛
            old_centroids = self.centroids.copy()

            # 3. 更新聚类中心
            self.centroids = self._get_new_centroids(X)

            # 4. 判断是否收敛 (中心不再移动)
            if np.all(old_centroids == self.centroids):
                break

        # 计算 Inertia (WCSS)
        self.inertia = self._calculate_inertia(X)

    def _create_clusters(self, X):
        labels = np.zeros(len(X))
        for idx, sample in enumerate(X):
            distances = [self._euclidean_distance(sample, centroid) for centroid in self.centroids]
            labels[idx] = np.argmin(distances)
        return labels

    def _get_new_centroids(self, X):
        centroids = np.zeros((self.k, X.shape[1]))
        for cluster_idx in range(self.k):
            # 找到属于当前簇的所有样本
            cluster_points = X[self.labels == cluster_idx]
            if len(cluster_points) > 0:
                centroids[cluster_idx] = np.mean(cluster_points, axis=0)
        return centroids

    def _calculate_inertia(self, X):
        inertia = 0
        for idx, sample in enumerate(X):
            centroid = self.centroids[int(self.labels[idx])]
            inertia += np.sum((sample - centroid) ** 2)
        return inertia



# 2. 聚类标签与真实标签对齐工具

# 因为聚类是无监督的，模型分出的簇 0,1,2 未必对应真实的类别 0,1,2
# 我们需要找到每个簇中最多的真实标签，作为该簇的代表标签
def align_labels(predicted_labels, true_labels):
    aligned_labels = np.zeros_like(predicted_labels)
    for cluster_idx in range(3):
        # 找到被预测为 cluster_idx 的所有样本的真实标签
        mask = (predicted_labels == cluster_idx)
        if np.sum(mask) > 0:
            true_labels_in_cluster = true_labels[mask]
            # 找到该簇中出现次数最多的真实标签
            most_frequent_label = np.bincount(true_labels_in_cluster).argmax()
            aligned_labels[mask] = most_frequent_label
    return aligned_labels


# ==========================================
# 3. 主程序运行
# ==========================================
if __name__ == "__main__":
    # 直接从 UCI 仓库读取 Iris 数据集
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    df = pd.read_csv(url, names=column_names)

    # 特征矩阵
    X = df.iloc[:, :-1].values

    # 标签处理：将字符串标签转换为数字 0, 1, 2
    species_map = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    y_true = df['class'].map(species_map).values

    # 训练 K-Means 模型
    kmeans = CustomKMeans(k=3, max_iters=100, random_state=42)
    kmeans.fit(X)

    # 评估 1: 簇内误差平方和 (Inertia)
    print("--- K-Means 聚类内部评估 ---")
    print(f"簇内误差平方和 (Inertia/WCSS): {kmeans.inertia:.4f}")

    # 评估 2: 聚类准确率 (Purity/Accuracy)
    aligned_predictions = align_labels(kmeans.labels, y_true)
    accuracy = np.mean(aligned_predictions == y_true)

    print("\n--- K-Means 聚类外部评估 (结合真实标签) ---")
    print(f"聚类准确率 (Clustering Accuracy): {accuracy:.4f}")
