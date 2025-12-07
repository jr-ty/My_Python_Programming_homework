
## Project 3: 鸢尾花数据分类与可视化 (Iris Classification & Visualization)

### 项目简介 (Introduction)

本项目基于经典的 **鸢尾花（Iris）数据集**，利用 Python 机器学习生态（Scikit-learn, Matplotlib, NumPy）实现了一套完整的分类与可视化工作流。

项目不仅实现了基础的二维分类边界对比，还深入探索了三维空间中的**线性决策平面**与**非线性决策曲面**的可视化技术，并通过“墙面投影法”直观展示了模型在空间中的概率分布。

#### 核心功能
* **数据探索**：箱线图与散点矩阵分析，辅助特征选择。
* **多模型对比 (2D)**：逻辑回归 (LR)、支持向量机 (SVM)、高斯过程 (GP) 的边界对比。
* **3D 线性边界**：绘制逻辑回归在三维特征空间中的决策平面。
* **3D 概率投影**：利用墙面投影技术展示三维概率场。
* **3D 非线性曲面 (Bonus)**：使用数值求解法绘制 SVM (RBF Kernel) 的隐函数曲面。

---

### 环境依赖 (Requirements)

本项目基于 **Python 3.13+** 开发。请确保安装以下依赖库：

* **核心库**：`numpy`, `pandas`, `scikit-learn`
* **绘图库**：`matplotlib`, `seaborn`
* **交互图表**：`plotly`

#### 快速安装
你可以使用 `pip` 一键安装所有依赖：

```bash
pip install numpy pandas scikit-learn matplotlib seaborn plotly
````

> **注意**：为了确保中文字符在 Matplotlib 图表中正常显示，代码中已内置了字体适配逻辑（优先使用 SimHei, Microsoft YaHei 或 Arial Unicode MS）。

-----

### 文件结构与说明 (File Structure)

```text
Project3/
├── README.md                   # 项目说明文档
├── data_preview.py             # [数据探索] 特征分布箱线图 & 散点矩阵
├── comparison.py               # [Task 1] 2D 多分类器边界对比 (LR/SVM/GP)
├── 3d_boundary.py              # [Task 2] 3D 线性决策平面 (Logistic Regression)
├── 3d_probability.py           # [Task 3] 3D 概率分布墙面投影
└── nonlinear.py                # [Task 4] 3D 非线性 SVM 决策曲面 (Bonus)
```

-----

###  运行指南 (Usage)

请按照以下顺序运行脚本以复现实验结果。

#### 1\. 数据探索与特征选择

运行 `data_preview.py` 查看数据分布。

```bash
python data_preview.py
```

  * **输出**：生成特征分布箱线图，并启动浏览器显示 Plotly 交互式散点图。
  * **分析**：用于确认 *Petal Length* 和 *Petal Width* 是最具区分度的特征。

#### 2\. Task 1: 2D 分类器对比

运行 `comparison.py` 对比不同模型。

```bash
python comparison.py
```

  * **输出**：一张包含 3 行 4 列的大图，展示逻辑回归、线性 SVM 和高斯过程的决策边界及各类别的概率热力图。

#### 3\. Task 2: 3D 线性决策平面

运行 `3d_boundary.py` 查看线性分割效果。

```bash
python 3d_boundary.py
```

  * **输出**：三维散点图，中间有一个灰色的半透明平面将两类数据分开。

#### 4\. Task 3: 3D 概率投影

运行 `3d_probability.py` 查看概率分布。

```bash
python 3d_probability.py
```

  * **输出**：三维空间图，在 XY、YZ、XZ 三个墙面上绘制了彩色的概率等高线投影。

#### 5\. Task 4: 非线性曲面 (Bonus)

运行 `nonlinear.py` 查看高阶可视化效果。

```bash
python nonlinear.py
```

  * **输出**：展示 SVM (RBF核) 生成的**弯曲决策曲面**，并结合了三视面投影。
  * *提示*：由于需要进行 3D 空间数值扫描，该脚本运行可能需要几秒钟，请耐心等待控制台进度提示。

-----

###  结果示例 (Results)

| 任务 | 描述 |
| :--- | :--- |
| **Task 1** | 逻辑回归生成直线边界，高斯过程生成平滑曲线边界。 |
| **Task 2** | 线性平面成功分割了 Setosa 和 Versicolor 类别。 |
| **Task 3** | 墙面投影清晰展示了概率从 0 到 1 的线性过渡。 |
| **Task 4** | 非线性 SVM 曲面呈现“山谷”状包裹数据，边缘拟合更精细。 |

-----