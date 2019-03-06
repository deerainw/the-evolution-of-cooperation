# coding=utf-8

"""
对结果进行统计的函数
"""

from pandas import DataFrame
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def camp_stats(df: DataFrame):
    # 在阵营维度上进行统计，如果每个阵营的人数相近、各种策略人群的占比平均、每个阵营的总金钱数相近的话，说明模拟样本足够大
    # 输出图表
    print("\n 各个阵营的人数：\n", df['camp'].value_counts())


def tactics_stats(df: DataFrame):
    """
    在策略维度上进行统计
    输出各种策略的人群的平均金钱数啊，绘制一个柱状图来展示

    -----
    :param df:
    :return:
    """

    stats_result = df.groupby(['tactics'], as_index=False).agg({'money': 'mean'})
    plt.title("采取各种策略的人群的平均金钱")
    plt.bar(stats_result['tactics'], stats_result['money'])
    plt.show()
