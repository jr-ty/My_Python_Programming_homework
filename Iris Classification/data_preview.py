import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# --- 1. 设置统一的绘图风格与中文字体 ---
plt.style.use('seaborn-v0_8-whitegrid')

# [关键修复] 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定义统一的颜色字典
color_dict = {0: '#1f77b4', 1: '#d62728', 2: '#2ca02c'}

# --- 2. 加载数据 ---
# 加载 Seaborn 内置的 iris 数据集
df = sns.load_dataset('iris')

# --- 3. 静态图表：箱线图 (Boxplot) ---
# 创建 2x2 的画布
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Iris 数据集特征分布概览 (箱线图)', fontsize=16)

# 特征列表
features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

# 循环绘制每个特征的箱线图
for i, feature in enumerate(features):
    row, col = i // 2, i % 2
    sns.boxplot(x='species', y=feature, data=df, ax=axes[row, col], palette="Set1")
    axes[row, col].set_title(f'{feature} 分布情况', fontsize=12)

plt.tight_layout()
plt.show()

# --- 4. 交互式图表：Plotly 散点图 ---
# Plotly 通常对中文支持较好，不需要额外设置字体（除非保存为静态图片）
fig = px.scatter_matrix(
    df,
    dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    color="species",
    title="Iris 数据集特征散点矩阵 (Scatter Matrix)",
    labels={col: col.replace('_', ' ').title() for col in df.columns}
)
fig.update_traces(diagonal_visible=False) # 对角线上不显示
fig.show()