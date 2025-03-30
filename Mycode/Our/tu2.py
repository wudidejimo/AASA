import matplotlib.pyplot as plt
import numpy as np


# 设置全局高分辨率参数（300 dpi）
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# 数据 scable annlight, ,UAV, SECURE SAAF, nosiy,our
labels = ['[4]', '[5]', '[6]', '[25]', '[37]', '[38]', 'Ours']
communication_cost = [1408,2784,  4608, 5376, 2656, 3136, 2912]  # 通信花销
message_round = [3, 3, 4, 6, 3, 5, 4]                           # 消息轮数

# 将标签转换为数值下标: 0,1,2,... 用于灵活控制柱子和折线位置
x = np.arange(len(labels))

# 柱子宽度
bar_width = 0.35

# 创建画布
fig, ax1 = plt.subplots(figsize=(8, 6))

# 1. 绘制柱状图：让柱子中心放在 x+0.5 (即每个整数区间 [n, n+1] 的中点)
bars_x = x + 0.5
bars = ax1.bar(bars_x, communication_cost, width=bar_width, color='C0', alpha=0.7,
               label='Communication cost(bit)')

# 设置左侧 y 轴（通信花销）
ax1.set_ylabel('Cost (bit)', color='C0')
ax1.tick_params(axis='y', labelcolor='C0')
ax1.set_ylim(0, 10000)                     # 范围 0 ~ 10000
ax1.set_yticks(range(0, 10001, 2000))      # 每 2000 为一个刻度

# 将 x 轴刻度设置为与柱子中心对齐
ax1.set_xticks(bars_x)
ax1.set_xticklabels(labels)

# 在柱子上方标注数值
for rect in bars:
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width() / 2.0,
             height + 50,  # 文字距离柱顶的距离可自行调节
             f'{height}',
             ha='center', va='bottom', fontsize=9, color='C0')

# 2. 创建右侧坐标轴，绘制折线图（消息轮数）
ax2 = ax1.twinx()
ax2.set_ylabel('Message round', color='C1')
ax2.tick_params(axis='y', labelcolor='C1')
ax2.set_ylim(0, 7)  # 根据轮数最高值 6 留一些余量

# 将折线图的 x 轴再向右偏移一些（例如 + bar_width），避免与柱状图重叠
line_x = bars_x 
line = ax2.plot(line_x, message_round, color='C1', marker='o', markersize=6,
                linewidth=2, label='Message round')

# 在折线图上标注数值
for xx, yy in zip(line_x, message_round):
    ax2.text(xx, yy + 0.2, f'{yy}', ha='center', va='bottom',
             color='C1', fontsize=9)

# 合并图例
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center',bbox_to_anchor=(0.35, 0.98), ncol=2)

# 保存为高分辨率的PNG和PDF（矢量图）格式
plt.savefig("communication.png", dpi=300, bbox_inches='tight')
plt.savefig("communication.pdf", bbox_inches='tight')


plt.tight_layout()
plt.show()
