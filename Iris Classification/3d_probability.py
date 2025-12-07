import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from mpl_toolkits.mplot3d import Axes3D

# --- 1. 风格与数据 ---
plt.style.use('seaborn-v0_8-whitegrid')

# [关键修复] 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

iris = load_iris()
mask = iris.target != 2
X = iris.data[mask][:, :3]
y = iris.target[mask]

clf = LogisticRegression(random_state=42)
clf.fit(X, y)

# --- 2. 设置绘图边界 ---
# 手动固定坐标轴范围，确保投影贴在“墙”上
x_min, x_max = 4.0, 7.5
y_min, y_max = 1.8, 4.8
z_min, z_max = 0.8, 5.5
res = 100 # 网格分辨率

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# --- 3. 绘制墙面投影 (Wall Projections) ---
# 定义一个辅助函数来画投影
def plot_projection(ax, xx, yy, zz, zdir, offset):
    """辅助函数：计算概率并画出 contourf"""
    # 将网格展平为 (n_samples, 3) 的坐标点
    grid = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
    # 预测概率
    probs = clf.predict_proba(grid)[:, 1].reshape(xx.shape)
    # 绘制等高线 (coolwarm: 蓝=0 -> 红=1)
    ax.contourf(xx if zdir!='x' else probs, # 这里利用 trick 适配不同轴
                yy if zdir!='y' else probs,
                zz if zdir!='z' else probs,
                zdir=zdir, offset=offset, cmap='coolwarm', alpha=0.6)

# A. 底部投影 (XY平面)
xx, yy = np.meshgrid(np.linspace(x_min, x_max, res), np.linspace(y_min, y_max, res))
zz_const = np.full_like(xx, z_min)
# 手动调用绘图 (因为 contourf 的参数传递比较特殊，直接写更直观)
grid_bottom = np.c_[xx.ravel(), yy.ravel(), zz_const.ravel()]
probs_bottom = clf.predict_proba(grid_bottom)[:, 1].reshape(xx.shape)
ax.contourf(xx, yy, probs_bottom, zdir='z', offset=z_min, cmap='coolwarm', alpha=0.5)

# B. 左侧投影 (YZ平面)
yy_side, zz_side = np.meshgrid(np.linspace(y_min, y_max, res), np.linspace(z_min, z_max, res))
grid_side = np.c_[np.full(yy_side.size, x_min), yy_side.ravel(), zz_side.ravel()]
probs_side = clf.predict_proba(grid_side)[:, 1].reshape(yy_side.shape)
ax.contourf(probs_side, yy_side, zz_side, zdir='x', offset=x_min, cmap='coolwarm', alpha=0.5)

# C. 背面投影 (XZ平面)
xx_back, zz_back = np.meshgrid(np.linspace(x_min, x_max, res), np.linspace(z_min, z_max, res))
grid_back = np.c_[xx_back.ravel(), np.full(xx_back.size, y_max), zz_back.ravel()]
probs_back = clf.predict_proba(grid_back)[:, 1].reshape(xx_back.shape)
ax.contourf(xx_back, probs_back, zz_back, zdir='y', offset=y_max, cmap='coolwarm', alpha=0.5)

# --- 4. 绘制中间的决策网格 (Wireframe) ---
w = clf.coef_[0]
b = clf.intercept_[0]
xx_surf, yy_surf = np.meshgrid(np.linspace(x_min, x_max, 20), np.linspace(y_min, y_max, 20))
zz_surf = -(w[0] * xx_surf + w[1] * yy_surf + b) / w[2]
# 裁剪超出范围的点
zz_surf[(zz_surf < z_min) | (zz_surf > z_max)] = np.nan
# 绘制蓝色线框
ax.plot_wireframe(xx_surf, yy_surf, zz_surf, color='#4169E1', alpha=0.4, label='Decision Plane')

# --- 5. 绘制原始数据点 ---
ax.scatter(X[y==0, 0], X[y==0, 1], X[y==0, 2], c='#1f77b4', s=50, edgecolors='k', label='类别 0')
ax.scatter(X[y==1, 0], X[y==1, 1], X[y==1, 2], c='#d62728', s=50, edgecolors='k', label='类别 1')

# --- 6. 设置 ---
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)
ax.set_xlabel('花萼长度 (Sepal Length)')
ax.set_ylabel('花萼宽度 (Sepal Width)')
ax.set_zlabel('花瓣长度 (Petal Length)')
ax.set_title('Task 3: 3D 概率分布投影 (Probability Projections)', fontsize=14)
ax.view_init(elev=25, azim=-50)
plt.legend()
plt.show()