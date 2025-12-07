import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

# --- 1. 统一风格与字体设置 ---
plt.style.use('seaborn-v0_8-whitegrid')

# [关键修复] 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 自定义三种颜色的列表 (蓝, 红, 绿)
class_colors = ['#1f77b4', '#d62728', '#2ca02c']
cmap_boundary = mcolors.ListedColormap(class_colors)

# --- 2. 数据准备 ---
iris = load_iris()
X = iris.data[:, 2:]  # 只使用最后两个特征 (Petal Length, Petal Width)
y = iris.target  # 包含 0, 1, 2 三类

# --- 3. 定义模型列表 ---
classifiers = {
    "Logistic Regression": LogisticRegression(C=1.0),
    "Linear SVM": SVC(kernel="linear", probability=True),
    "Gaussian Process": GaussianProcessClassifier(1.0 * RBF(1.0))
}

# --- 4. 绘图准备 ---
# 创建网格用于绘制背景颜色
h = 0.05
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

n_classifiers = len(classifiers)
# 创建大图：行数=模型数，列数=4 (1个决策图 + 3个概率图)
fig, axes = plt.subplots(n_classifiers, 4, figsize=(20, 5 * n_classifiers))

# --- 5. 循环训练并绘图 ---
for i, (name, clf) in enumerate(classifiers.items()):
    print(f"正在训练模型: {name}...")
    clf.fit(X, y)

    # 获取当前行的坐标轴对象
    row_axes = axes[i] if n_classifiers > 1 else axes

    # [第1列] 绘制整体决策边界
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    row_axes[0].imshow(Z, extent=(xx.min(), xx.max(), yy.min(), yy.max()), origin='lower',
                       cmap=cmap_boundary, alpha=0.4)  # 背景色半透明
    # 绘制原始数据点
    row_axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_boundary, edgecolors='k', s=50)
    row_axes[0].set_title(f"{name}\n决策边界 (Decision Boundary)")
    row_axes[0].set_ylabel('Petal Width')

    # [第2-4列] 绘制每一类的概率分布
    probs = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])
    probs = probs.reshape(xx.shape[0], xx.shape[1], 3)

    for j in range(3):
        ax = row_axes[j + 1]
        # 创建单色渐变 colormap (白色 -> 该类的主色)
        cmap_prob = mcolors.LinearSegmentedColormap.from_list(f'c{j}', ['#ffffff', class_colors[j]])

        # 绘制概率等高线
        contour = ax.contourf(xx, yy, probs[:, :, j], levels=20, cmap=cmap_prob, alpha=0.8)
        # 绘制数据点 (为了对比，还是画上)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_boundary, edgecolors='k', s=20, alpha=0.6)

        ax.set_title(f"类别 {j} ({iris.target_names[j]}) 概率")
        if i == n_classifiers - 1:  # 只在最后一行加X轴标签
            ax.set_xlabel('Petal Length')

plt.tight_layout()
plt.show()