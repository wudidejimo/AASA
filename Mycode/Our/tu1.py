import numpy as np
import matplotlib.pyplot as plt

# 设置全局高分辨率参数（300 dpi）
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
# 研究编号及Ours方法
labels = ["[4]", "[5]", "[36]", "[25]", "[37]", "[38]", "Ours"]
#  scable  annlight ,UAV, SECURE ,SAAF ,nosiy ,our
# 每个研究下的 "In Theory" 和 "Simulation" 两组数据
NodeA = {
    "In Theory":  [ 0    ,  16.2451, 22.5997, 27.8013, 22.0619, 0,       1.1325],
    "Simulation": [ 2.4215, 18.3573, 24.6423, 29.0346, 23.9456, 2.0850,  2.2356]
}
NodeB = {
    "In Theory":  [0.9688,  14.9742, 22.4613, 18.3326,  7.6413, 3.4950, 3.1649],
    "Simulation": [3.4792,  15.3562, 24.3562, 19.3546,  8.3562, 8.7781, 5.3344]
}
GWN = {
    "In Theory":  [1.1360,  1.3840, 15.9430,  11.5191, 14.5590, 2.6296,  1.9506],
    "Simulation": [4.0226,  3.3452, 17.3532,  14.4637, 15.3563, 4.0078,  5.5553]
}

# X轴的位置
x = np.arange(len(labels))

# 柱状图的宽度
bar_width = 0.3

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))



# 绘制 In Theory 数据 (左侧柱子)
ax.bar(x - bar_width/1.5, NodeA["In Theory"], width=bar_width, label="NodeA", color="dodgerblue")
ax.bar(x - bar_width/1.5, NodeB["In Theory"], width=bar_width, bottom=NodeA["In Theory"], color="coral", label="NodeB")
ax.bar(x - bar_width/1.5, GWN["In Theory"], width=bar_width, bottom=np.array(NodeA["In Theory"]) + np.array(NodeB["In Theory"]), color="gray", label="GWN")

# 绘制 Simulation 数据 (右侧柱子)
ax.bar(x + bar_width/1.5, NodeA["Simulation"], width=bar_width, color="dodgerblue")
ax.bar(x + bar_width/1.5, NodeB["Simulation"], width=bar_width, bottom=NodeA["Simulation"], color="coral")
ax.bar(x + bar_width/1.5, GWN["Simulation"], width=bar_width, bottom=np.array(NodeA["Simulation"]) + np.array(NodeB["Simulation"]), color="gray")

# 添加 In Theory 和 Simulation 的标签 (90度旋转显示)
for i in range(len(labels)):
    ax.text(x[i] - bar_width/1.5, -19, "In Theory", ha="center", fontsize=10, color="black", rotation=90)
    ax.text(x[i] + bar_width/1.5, -19, "Simulation", ha="center", fontsize=10, color="black", rotation=90)
    if i < len(labels) - 1:
        #ax.axvline(x[i]+ 5*bar_width/3, color='black', linestyle='dashed', linewidth=0.8, alpha=0.5)
        x_pos = x[i] + 5 * bar_width / 3  # 线的 x 位置
    ymin = 0  # 线的起点 (y轴)
    ymax = -19  # 线的终点 (y轴)
    ax.vlines(x_pos, ymin=ymin, ymax=ymax, color='black', linestyle='dashed', linewidth=0.8, alpha=0.5)


# 在 0 轴画一条横线
ax.axhline(y=0, color='black', linewidth=1.5)

# 设置 X 轴标签
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=0, ha="center")  # 研究编号正常显示

# 隐藏最下面的 X 轴
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks_position('none')  # 隐藏底部刻度




# 设置 Y 轴
ax.set_ylabel("Cost (ms)", labelpad=10)

ax.set_ylim(-20, 80)  # 适应底部标签的显示

# 设置 Y 轴刻度间隔为 5
ax.set_yticks(np.arange(0, 81, 10))


# 调整图例（Legend）到左上角，并横向排序
ax.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95), ncol=3, frameon=True)

# 保存为高分辨率的PNG和PDF（矢量图）格式
plt.savefig("computation.png", dpi=300, bbox_inches='tight')
plt.savefig("computation.pdf", bbox_inches='tight')


# 显示图表
plt.show()




