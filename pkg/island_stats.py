# coding=utf-8

"""
对结果进行统计的函数
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
from pkg.template import Island, Human
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def get_result(island: Island):
    """
    统计模拟完成后岛上所有人的情况

    -----
    :param island: 岛屿
    :return: 返回一个 DataFrame，三列分别代表每个人的阵营、策略和金钱
    """
    all_camp = list()
    all_tactics = list()
    all_money = list()

    length = island.length
    for x in range(length):
        for y in range(length):
            if island.grid[x, y].__class__.__name__ == 'Human':
                this_guy: Human = island.grid[x, y]
                # 收集每一个人的信息
                all_camp.append(this_guy.camp)
                all_tactics.append(this_guy.tactics)
                all_money.append(this_guy.money)

    all_camp = np.array(all_camp)
    all_tactics = np.array(all_tactics)
    all_money = np.array(all_money)

    result_mx = np.vstack((all_camp,
                           all_tactics,
                           all_money)).T

    result_df = pd.DataFrame(data=result_mx, columns=["camp", "tactics", "money"])
    result_df['money'] = result_df['money'].astype('int')

    return result_df


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
