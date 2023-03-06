import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from getdata import df_merged, result_F
from pandastable import Table


def add_legend(ax, legend_labels):
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[i]) for i in range(len(legend_labels))]
    ax.legend(handles, legend_labels)


def create_chart(ax, manager_data, labels, legend_labels):
    datas = []
    for column in legend_labels:
        data = manager_data[column].tolist()
        datas.append(data)
    data = {
        'labels': labels,
        'datas': datas,
        'legend_labels': legend_labels,
    }
    create_multi_bars(ax, data)


def create_multi_bars(ax, data):
    """
    ax : 绘图坐标轴对象
    labels : x轴坐标标签序列
    datas ：数据集，二维列表，要求列表每个元素的长度必须与labels的长度一致
    p_title : 柱状图标题
    tick_step ：默认x轴刻度步长为1，通过tick_step可调整x轴刻度步长。
    group_gap : 柱子组与组之间的间隙，最好为正值，否则组与组之间重叠
    bar_gap ：每组柱子之间的空隙，默认为0，每组柱子紧挨，正值每组柱子之间有间隙，负值每组柱子之间重叠
    """
    labels, datas, legend_labels = data['labels'], data['datas'],  data['legend_labels']
    x = np.arange(len(labels)) * TICK_STEP
    group_num = len(datas)
    group_width = TICK_STEP - GROUP_GAP
    bar_span = group_width / group_num
    bar_width = bar_span - BAR_GAP

    # 绘制柱子
    for i in range(len(datas)):
        for index, value in enumerate(datas[i]):
            ax.bar(x[index] + i * bar_span, value, bar_width, label=labels[index], color=COLORS[i], capsize=0)
            ax.text(x[index] + i * bar_span, value, str(value), ha='center', va='bottom', color='black')

    # 设置标题和坐标轴
    ticks = x + (group_width - bar_span) / 2
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.tick_params(axis='y', which='both', length=0)
    ax.set_yticklabels([])

    # 添加图例
    add_legend(ax, legend_labels)


def create_work_hours_chart(ax, manager_data, labels):
    create_chart(ax, manager_data, labels, CHART_LEGEND_HOURS[0])
    ax.set_title(CHART_LEGEND_HOURS[1])


def create_project_status_chart(ax, manager_data, labels):
    create_chart(ax, manager_data, labels, CHART_LEGEND_STATUS[0])
    ax.set_title(CHART_LEGEND_STATUS[1])


def update_chart():
    # 清空Frame
    for widget in chart_frame_top.winfo_children():
        widget.destroy()
    for widget in chart_frame_bottom.winfo_children():
        widget.destroy()
    # 获取选中的项目经理
    manager = selected_manager.get()
    # 过滤数据，只保留选中的项目经理
    manager_data = df_merged.loc[df_merged['项目经理'] == manager]
    labels = []
    for i, row in manager_data.iterrows():
        label = f"{row['项目名称']}\n{row['项目编号']}"
        labels.append(label)

    ax_top.clear()
    create_work_hours_chart(ax_top, manager_data, labels)
    canvas_top = FigureCanvasTkAgg(fig_top, master=chart_frame_top)
    canvas_top.draw()
    canvas_top.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ax_bottom.clear()
    create_project_status_chart(ax_bottom, manager_data, labels)
    canvas_bottom = FigureCanvasTkAgg(fig_bottom, master=chart_frame_bottom)
    canvas_bottom.draw()
    canvas_bottom.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 生成字体微软雅黑
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c']
CHART_LEGEND_HOURS = [['申报工时', '确认工时', '差值'], '本月工时状态']
CHART_LEGEND_STATUS = [['当月项目完成度', '项目总进度', '当月前项目完成度'], '本月项目完成状态']
TICK_STEP = 3
GROUP_GAP = 0.5
BAR_GAP = 0.1

root = tk.Tk()
root.geometry("800x600")

# 新建一个Frame用于存放下拉菜单和更新按钮
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=10)


managers = list(df_merged['项目经理'].unique())
managers.insert(0, managers[0])  # 将第一个项目经理插入到列表的第一个位置
selected_manager = tk.StringVar()
selected_manager.set(managers[0])

# 下拉菜单
manager_dropdown = ttk.OptionMenu(input_frame, selected_manager, *managers)
manager_dropdown.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.CENTER)

# 更新按钮
update_button = tk.Button(input_frame, text="更新图表", command=update_chart)
update_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.CENTER)

chart_frame_top = tk.Frame(root)
chart_frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

chart_frame_bottom = tk.Frame(root)
chart_frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

fig_top = plt.Figure(figsize=(6, 4), dpi=100)
ax_top = fig_top.add_subplot(111)

fig_bottom = plt.Figure(figsize=(6, 4), dpi=100)
ax_bottom = fig_bottom.add_subplot(111)


# 初始化图表
update_chart()

# 运行Tkinter主循环
root.mainloop()
