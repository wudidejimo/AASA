import numpy as np
import matplotlib.pyplot as plt

# 设置高分辨率
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

labels = ["[4]", "[5]", "[36]", "[25]", "[37]", "[38]", "Ours"]

NodeA = {
    "In Theory":  [16.2451, 22.0619, 22.5997, 27.8013, 0,     0,         1.1325],
    "Simulation": [18.3573, 23.9456, 24.6423, 29.0346, 2.4215, 2.0850, 2.2356]
}
NodeB = {
    "In Theory":  [14.9742, 7.6413, 22.4613, 18.3326, 10.6568, 3.4950, 3.1649],
    "Simulation": [15.3562, 8.3562, 24.3562, 19.3546, 15.4792, 8.7781, 5.3344]
}
GWN = {
    "In Theory":  [1.3840, 14.5590, 15.9430, 11.5191, 1.1360, 2.6296,   1.9506],
    "Simulation": [3.3452, 15.3563, 17.3532, 14.4637, 7.0226, 4.0078,   5.5553]
}

# 缩短X轴跨度
x = np.linspace(0, len(labels) - 1, len(labels)) * 0.8
bar_width = 0.3

fig, ax = plt.subplots(figsize=(7, 6))  # 缩窄图宽

# 绘制 In Theory
ax.bar(x - bar_width/1.5, NodeA["In Theory"], width=bar_width, label="NodeA", color="dodgerblue")
ax.bar(x - bar_width/1.5, NodeB["In Theory"], width=bar_width, bottom=NodeA["In Theory"], color="coral", label="NodeB")
ax.bar(x - bar_width/1.5, GWN["In Theory"], width=bar_width, 
       bottom=np.array(NodeA["In Theory"]) + np.array(NodeB["In Theory"]), color="gray", label="GWN")

# 绘制 Simulation
ax.bar(x + bar_width/1.5, NodeA["Simulation"], width=bar_width, color="dodgerblue")
ax.bar(x + bar_width/1.5, NodeB["Simulation"], width=bar_width, bottom=NodeA["Simulation"], color="coral")
ax.bar(x + bar_width/1.5, GWN["Simulation"], width=bar_width, 
       bottom=np.array(NodeA["Simulation"]) + np.array(NodeB["Simulation"]), color="gray")

# 添加文字标签
for i in range(len(labels)):
    ax.text(x[i] - bar_width/1.5, -18.5, "In Theory", ha="center", fontsize=9, rotation=90)
    ax.text(x[i] + bar_width/1.5, -18.5, "Simulation", ha="center", fontsize=9, rotation=90)
    if i < len(labels) - 1:
        x_pos = x[i] + 5 * bar_width / 3
        ax.vlines(x_pos, ymin=0, ymax=-18.5, color='black', linestyle='dashed', linewidth=0.8, alpha=0.5)

# 横线
ax.axhline(y=0, color='black', linewidth=1.5)

# 设置X轴
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=0, ha="center")
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks_position('none')

# 设置Y轴
ax.set_ylabel("Cost (ms)")
ax.set_ylim(-20, 80)
ax.set_yticks(np.arange(0, 81, 10))

# 图例
ax.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95), ncol=3, frameon=True)

# 保存图像
plt.savefig("Cost_Comparison_ShortX.png", dpi=300, bbox_inches='tight')
plt.savefig("Cost_Comparison_ShortX.pdf", bbox_inches='tight')

plt.show()
