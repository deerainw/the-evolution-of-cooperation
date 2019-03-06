# coding=utf-8

"""
项目内用到的类模板
"""

import numpy as np
import pandas as pd
import random


class Ground(object):
    """
    类：地面
    -----

    说明
    -----
    岛屿上的地面，显示为 . 一个点
    """
    def __repr__(self):
        return "."


class Island(object):
    """
    类：岛屿

    -----
    """
    def __init__(self, length: int = 10):
        """
        初始化岛屿

        :param length: 边界长度
        """
        self.length = length

        # 初始化时全部填充为地面
        self.grid = np.empty((self.length, self.length), Ground)
        self.grid[:, :] = Ground()

    def __repr__(self):
        return str(self.grid)

    def set_human(self, num: int, camp: list, tactics: list, money: int):
        """
        往 Island.grip 上放置人类对象，使用的实参都是 main.py 模块开头的参数

        ----------
        :param num: 放置人类的数量
        :param camp: 阵营列表
        :param tactics: 策略列表
        :param money: 初始金钱数

        -----
        :return: 无返回值，改变 Island.grid 的状态
        """
        x = np.random.randint(0, self.length, size=num)
        y = np.random.randint(0, self.length, size=num)
        # 不能一次性产生所有人类，这样所有人的阵营和策略随机结果都会相同
        for i in range(num):
            self.grid[x[i], y[i]] = Human(camp, tactics, money)
            self.grid[x[i], y[i]].xy = [x[i], y[i]]  # 每个人的 xy 类属性代表这个人在岛屿上的位置
            self.grid[x[i], y[i]].island = self


class Human(object):
    """
    类：人类
    -----

    属性
    -----
    - camp 阵营
    - tactics 策略
    - money 初始金钱
    - xy 坐标，一个 list，这个属性在 Island.set_human() 里第一次赋值

    方法
    -----
    """
    def __init__(self, camp: list, tactics: list, money: int,
                 xy: list = None,
                 island: Island = None):
        """
        初始化一个人类实例时，给这个人随机选择一个阵营，并随机选择一种策略。
        每个人的初始金钱数相同。

        -----
        :param camp: 每个元素是一个阵营的名字，每个人出生时随机选择其中一个阵营
        :param tactics: 每个元素是一种策略的名字，每个人出生时随机选择其中一种策略
        :param money: 初始金钱数，每个人的初始金钱相同
        :param xy: 初始为 None，在 Island.set_human() 里第一次赋值
        :param island: 这个人类属于哪个岛屿

        -----
        :return: 一个人类实例
        """
        self.camp = random.sample(camp, 1)[0]
        self.tactics = random.sample(tactics, 1)[0]
        self.money = money
        self.xy = xy
        self.island = island

    def __repr__(self):
        return "@"

    def edge(self, x: int, y: int):
        """
        给定一个目标坐标的 x 和 y，判断那个目标位置有没有超出边界

        :param x: x 坐标
        :param y: y 坐标
        :return: 返回一个 bool 值，反映目标坐标有没有超出边界
        """
        not_edge_x = (x >= 0) and (x < self.island.length)
        not_edge_y = (y >= 0) and (y < self.island.length)
        not_edge = not_edge_x and not_edge_y
        return not_edge

    def move(self):
        """
        人类：随机移动

        * 随机生成移动增量，获得新位置坐标
        * 如果新位置没有超出边界并且新位置没有被占据，就可以移动到新位置
        """
        # 移动坐标增量
        move_x = random.randint(-1, 1)
        move_y = random.randint(-1, 1)
        # 只有满足以下条件的时候才可以发生移动!
        new_x = self.xy[0] + move_x
        new_y = self.xy[1] + move_y
        # 判断新位置是否超出边界
        not_edge = self.edge(new_x, new_y)
        if not_edge:
            # 新位置没有被占据
            is_ground = isinstance(self.island.grid[new_x, new_y], Ground)
            if is_ground:
                # 这个人原来的位置填充为地面
                self.island.grid[self.xy[0], self.xy[1]] = Ground()
                # 人类自身的坐标属性改变
                self.xy[0] = new_x
                self.xy[1] = new_y
                # 新的位置用同一个人类对象填充
                self.island.grid[self.xy[0], self.xy[1]] = self
            else:
                pass

    def search(self):
        """
        人类：寻找周围的人类，随机选择一个发生接触的对象

        寻找周围八个格子内的人类，如果周围有一个或多个人的话，再随机选中其中一个

        返回选择的人类的坐标？
        """
        surround_people = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not(i == 0 and j == 0):
                    search_x = self.xy[0] + i
                    search_y = self.xy[1] + j
                    # 判断搜寻的位置是否超出边界
                    not_edge = self.edge(search_x, search_y)
                    if not_edge:
                        if isinstance(self.island.grid[search_x, search_y], Human):
                            surround_people.append(self.island.grid[search_x, search_y])

        # 随机选择一个人
        if len(surround_people) == 0:
            return None
        else:
            target_xy = random.sample(surround_people, 1)[0].xy
            return target_xy

    def check_camp(self, another_man: 'Human'):
        """
        判断 self 和 another_man 的阵营是否相同，返回布尔值
        :param another_man: 和 self 发生接触的人类对象
        :return: bool，代表双方阵营是否相同
        """
        if self.camp == another_man.camp:
            return True
        else:
            return False

    def make_a_choice(self, same_camp: bool):
        """
        根据自身的行为主义(tactics)以及双方是否同一个阵营来做出自己对于本次接触的选择(合作或欺骗)
        :param same_camp: bool，双方是否同一阵营
        :return: string, "cooperation" or "defection"
        """
        behavior = "No behavior"

        if self.tactics == "阵营虚无主义":
            behavior = random.sample(["cooperation", "defection"], 1)[0]

        if self.tactics == "阵营沙文主义" and same_camp:
            behavior = "cooperation"

        if self.tactics == "阵营沙文主义" and (not same_camp):
            behavior = "defection"

        if self.tactics == "极端反沙文主义" and same_camp:
            behavior = "defection"

        if self.tactics == "极端反沙文主义" and (not same_camp):
            behavior = "cooperation"

        return behavior

    def reward(self, choice1: str, choice2: str):
        """
        计算本次接触后自己的收益变化并更新自己的 money 属性，无返回值
        :param choice1: 自己的选择
        :param choice2: 对方的选择
        :return: None
        """
        reward_value = np.array([[3, 0], [5, -1]])
        col_name = ["cooperation", "defection"]
        idx_name = ["cooperation", "defection"]
        reward_matrix = pd.DataFrame(data=reward_value, index=idx_name, columns=col_name)
        self.money += reward_matrix.loc[choice1, choice2]

    def contact(self, another_man: 'Human'):
        """
        与另一个人类对象发生接触，更新双方的收益，无返回值
        :param another_man: 与自身发生本次接触的另一个人类对象
        :return: None
        """
        # 判断双方时候是相同阵营
        same_camp = self.check_camp(another_man)
        # 双方选择本次接触是合作还是欺骗
        self_choice = self.make_a_choice(same_camp)
        other_choice = another_man.make_a_choice(same_camp)
        # 计算收益，更新双方的 money 属性
        self.reward(self_choice, other_choice)
        another_man.reward(other_choice, self_choice)
