# coding=utf-8

"""
The Evolution of Cooperation 主程序

-----
"""

from pkg.template import Island, Human
from pkg.island_stats import tactics_stats, camp_stats, get_result
import numpy as np
import pandas as pd

# 模拟参数
days = 100  # 持续天数
island_len = 20  # 边界长度
human_amount = int(island_len**2 / 3)  # 人类总数量
camp_list = ["魏", "蜀", "吴", "晋"]  # 阵营列表
tactics_list = ["阵营虚无主义", "阵营沙文主义", "极端反沙文主义"]  # 策略列表
init_money = 0  # 每个人的初始金钱数


def day_after_day(day: int, island: Island):
    """
    主函数
    -----

    Parameters
    -----
    :param day: 当前天数
    :param island: 岛屿对象
    """

    # 弱引用人类对象列表无法生存，所以以下代码改回使用循环

    # noinspection PyUnusedLocal
    this_guy: Human  # 上一行的注释用来禁用 pycharm 对未使用变量的警告

    # 每个人都轮流搜索一下四周的人，四周有人的话随机选一个来接触
    for x in range(island_len):
        for y in range(island_len):
            if island.grid[x, y].__class__.__name__ == 'Human':
                this_guy = island.grid[x, y]
                target_xy = this_guy.search()
                if target_xy is not None:
                    this_guy.contact(island.grid[target_xy[0], target_xy[1]])

    # 每个人轮流移动
    for x in range(island_len):
        for y in range(island_len):
            if island.grid[x, y].__class__.__name__ == 'Human':
                this_guy = island.grid[x, y]
                this_guy.move()

    # 输出岛屿状态
    print("第 " + str(day) + " 天")
    print(island)


if __name__ == "__main__":
    # 初始化岛屿
    bali = Island(length=island_len)
    # 放置人类
    bali.set_human(num=human_amount,
                   camp=camp_list,
                   tactics=tactics_list,
                   money=init_money)
    # 运行主函数
    for i in range(1, days):
        day_after_day(day=i, island=bali)

    # 获得结果
    df_result = get_result(bali)
    camp_stats(df_result)
    tactics_stats(df_result)
