#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from kanren import *
from kanren.core import lall


def left(q, p, list):
    return membero((q, p), zip(list, list[1:]))

def next(q, p, list):  # p q 相邻意味着要么p在q左边，要么q在p左边
    return conde([left(q, p, list)], [left(p, q, list)])


houses = var()

rules_zebraproblem = lall(
    (membero, ('Britain', var(), var(), var(), 'red'), houses),  # 英国人住在红房子里
    (membero, ('Spain', var(), var(), 'dog', var()), houses),  # 西班牙人养了一条狗
    (membero, ('Japan', 'painter', var(), var(), var()), houses),  # 日本人是一个油漆工
    (membero, ('Italy', var(), 'tea', var(), var()), houses),  # 意大利人喝茶。
    (membero, (var(), 'Photographer', var(), 'snail', var()), houses),  # 摄影师养了一只蜗牛
    (membero, (var(), 'diplomat', var(), var(), 'yellow'), houses),  # 外交官住在黄房子里
    (membero, (var(), var(), 'coffee', var(), 'green'), houses),  # 喜欢喝咖啡的人住在绿房子里
    (membero, (var(), 'Violinist', 'juice', var(), var()), houses),  # 小提琴家喜欢喝橘子汁

    (eq, (('Norwegian', var(), var(), var(), var())
        , var(), var(), var(), var()), houses),  # 挪威人住在左边的第一个房子里

    (eq, (var(), var(),(var(), var(), 'milk', var(), var()),
        var(), var()), houses),  # 中间那个房子的人喜欢喝牛奶

(left,  # 绿房子在白房子的右边
 (var(), var(), var(), var(), 'green'),
 (var(), var(), var(), var(), 'white'),
 houses),

(next, ('Norwegian', var(), var(), var(), var()),
 (var(), var(), var(), var(), 'blue'), houses),  # 挪威人住在蓝房子旁边。
 
(next, (var(), 'physician', var(), var(), var()),
 (var(), var(), var(), 'fox', var()), houses),   # 养狐狸的人所住的房子与医生的房子相邻

(next, (var(), 'diplomat', var(), var(), var()),
 (var(), var(), var(), 'horse', var()), houses),  # 养马的人所住的房子与外交官的房子相邻

(left,  # 绿房子在白房子的右边
 (var(), var(), var(), var(), 'green'),
 (var(), var(), var(), var(), 'white'),
 houses),

(next, ('Norwegian', var(), var(), var(), var()),
 (var(), var(), var(), var(), 'blue'), houses),  # 挪威人住在蓝房子旁边。

(next, (var(), 'physician', var(), var(), var()),  # 养狐狸的人所住的房子与医生的房子相邻
 (var(), var(), var(), 'fox', var()), houses),

(next, (var(), 'diplomat', var(), var(), var()),  # 养马的人所住的房子与外交官的房子相邻
 (var(), var(), var(), 'horse', var()), houses),

(membero, (var(), var(), var(), 'zebra', var()), houses),  # 有人养斑马

(membero, (var(), var(), 'water', var(), var()), houses)  # 有人喝水

)


solutions = run(0, houses, rules_zebraproblem) 

if len(solutions):
    zebra_owner = ""
    water_drinker = ""
    for i in solutions[0]:
        if "zebra" in i:
            zebra_owner = i[0]  # 找到斑马的主人
        if "water" in i:
            water_drinker = i[0]  # 找到喝矿泉水的人
        print(i)

    print('\nzebra_owner:\t\t' + zebra_owner)  # 打印结果
    print('water_drinker:\t' + water_drinker)

else:
    print("no answer")
