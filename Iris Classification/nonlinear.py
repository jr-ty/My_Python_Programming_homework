import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.svm import SVC
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

# --- 2. 训练非线性模型 (RBF Kernel SVM) ---
print("正在训练 SVM 模型...")
clf = SVC(kernel='rbf', C=10, gamma='auto', probability=True, random_state=42)
clf.fit(X, y)

# --- 3. 绘图范围 ---
x_min, x_max = 3.8, 7.5
y_min, y_max = 1.5, 5.0
z_min, z_max = 0.5, 5.5

fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# --- 4. 核心：数值求解非线性曲面 Z ---
res_surf = 30 # 曲面分辨率
xx_surf, yy_surf = np.meshgrid(np.linspace(x_min, x_max, res_surf),
                               np.linspace(y_min, y_max, res_surf))
zz_surf = np.zeros_like(xx_surf)
zz_surf[:] = np.nan

# 在 Z 轴方向扫描寻找决策边界 (decision_function = 0)
z_scan = np.linspace(z_min, z_max, 100)

print("正在计算非线性 3D 曲面，请稍候...")
for i in range(res_surf):
    for j in range(res_surf):
        # 构造扫描线
        scan_points = np.c_[np.full(100, xx_surf[i, j]), np.full(100, yy_surf[i, j]), z_scan]
        # 计算距离
        dists = clf.decision_function(scan_points)
        # 寻找符号翻转点 (即过零点)
        crossings = np.where(np.diff(np.sign(dists)))[0]
        if len(crossings) > 0:
            idx = crossings[0]
            # 线性插值求精确的 z
            d1, d2 = dists[idx], dists[idx+1]
            z1, z2 = z_scan[idx], z_scan[idx+1]
            zz_surf[i, j] = z1 + (z2 - z1) * (-d1 / (d2 - d1))

# 绘制曲面 (使用 viridis 颜色，半透明)
surf = ax.plot_surface(xx_surf, yy_surf, zz_surf, cmap='viridis', alpha=0.6,
                       rstride=1, cstride=1, edgecolor='none')
# 添加线框增强立体感
ax.plot_wireframe(xx_surf, yy_surf, zz_surf, color='black', alpha=0.15, rstride=3, cstride=3)

# --- 5. 绘制墙面投影 (含黑色轮廓线) ---
res_proj = 50
# A. 底部投影
xx, yy = np.meshgrid(np.linspace(x_min, x_max, res_proj), np.linspace(y_min, y_max, res_proj))
grid_bottom = np.c_[xx.ravel(), yy.ravel(), np.full_like(xx.ravel(), z_min)]
probs_bottom = clf.predict_proba(grid_bottom)[:, 1].reshape(xx.shape)
ax.contourf(xx, yy, probs_bottom, zdir='z', offset=z_min, cmap='coolwarm', alpha=0.5)
ax.contour(xx, yy, probs_bottom, levels=[0.5], zdir='z', offset=z_min, colors='black', linewidths=2) # 黑色分界线

# B. 左侧投影
yy_side, zz_side = np.meshgrid(np.linspace(y_min, y_max, res_proj), np.linspace(z_min, z_max, res_proj))
grid_side = np.c_[np.full(yy_side.size, x_min), yy_side.ravel(), zz_side.ravel()]
probs_side = clf.predict_proba(grid_side)[:, 1].reshape(yy_side.shape)
ax.contourf(probs_side, yy_side, zz_side, zdir='x', offset=x_min, cmap='coolwarm', alpha=0.5)
ax.contour(probs_side, yy_side, zz_side, levels=[0.5], zdir='x', offset=x_min, colors='black', linewidths=2)

# C. 背面投影
xx_back, zz_back = np.meshgrid(np.linspace(x_min, x_max, res_proj), np.linspace(z_min, z_max, res_proj))
grid_back = np.c_[xx_back.ravel(), np.full(xx_back.size, y_max), zz_back.ravel()]
probs_back = clf.predict_proba(grid_back)[:, 1].reshape(xx_back.shape)
ax.contourf(xx_back, probs_back, zz_back, zdir='y', offset=y_max, cmap='coolwarm', alpha=0.5)
ax.contour(xx_back, probs_back, zz_back, levels=[0.5], zdir='y', offset=y_max, colors='black', linewidths=2)

# --- 6. 绘制数据点 ---
ax.scatter(X[y==0, 0], X[y==0, 1], X[y==0, 2], c='#1f77b4', s=40, edgecolors='k', label='类别 0')
ax.scatter(X[y==1, 0], X[y==1, 1], X[y==1, 2], c='#d62728', s=40, edgecolors='k', label='类别 1')

# --- 7. 设置 ---
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)
ax.set_xlabel('花萼长度 (Sepal Length)')
ax.set_ylabel('花萼宽度 (Sepal Width)')
ax.set_zlabel('花瓣长度 (Petal Length)')
ax.set_title('Bonus Task: 非线性 SVM 曲面 + 三视面投影', fontsize=16)
ax.view_init(elev=25, azim=-55)

plt.legend()
plt.tight_layout()
plt.show()