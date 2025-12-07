import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from mpl_toolkits.mplot3d import Axes3D

# --- 1. 统一风格与字体设置 ---
plt.style.use('seaborn-v0_8-whitegrid')

# [关键修复] 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# --- 2. 数据准备 (二分类: 0 vs 1) ---
iris = load_iris()
mask = iris.target != 2 # 排除类别2
X = iris.data[mask][:, :3] # 取前3个特征
y = iris.target[mask]

# --- 3. 模型训练 ---
clf = LogisticRegression(random_state=42)
clf.fit(X, y)

# --- 4. 计算决策平面 ---
# 网格范围
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.2),
                     np.arange(y_min, y_max, 0.2))

# 提取系数: w0*x + w1*y + w2*z + b = 0 -> z = -(w0*x + w1*y + b)/w2
w = clf.coef_[0]
b = clf.intercept_[0]
z = -(w[0] * xx + w[1] * yy + b) / w[2]

# --- 5. 3D 绘图 ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制半透明的灰色平面
ax.plot_surface(xx, yy, z, alpha=0.5, color='gray', rstride=100, cstride=100)

# 绘制数据点 (使用统一的蓝/红配色)
ax.scatter(X[y==0, 0], X[y==0, 1], X[y==0, 2], c='#1f77b4', s=60, edgecolors='k', label='类别 0 (Setosa)')
ax.scatter(X[y==1, 0], X[y==1, 1], X[y==1, 2], c='#d62728', s=60, edgecolors='k', label='类别 1 (Versicolor)')

# 设置标签和标题
ax.set_xlabel('花萼长度 (Sepal Length)')
ax.set_ylabel('花萼宽度 (Sepal Width)')
ax.set_zlabel('花瓣长度 (Petal Length)')
ax.set_title('Task 2: 3D 线性决策边界 (Linear Decision Boundary)', fontsize=14)

# 调整初始视角
ax.view_init(elev=20, azim=30)
plt.legend()
plt.show()