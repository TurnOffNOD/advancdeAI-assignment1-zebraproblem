#!-*- encoding:utf8 -*-

from kanren import run, eq, membero, var, conde
from kanren import Relation, facts
from kanren.core import lall
import time

# Logical Programming
def equality_check():
    x = var()
    run(1, x, eq(x, 5))


def equality_check_with2facts():
    x = var()
    z = var()
    run(1, x, eq(x, z), eq(z, 3))


def member_check():
    x = var()
    run(2, x, membero(x, (1, 2, 3)),  # x is a member of (1, 2, 3) #x是（1,2,3）的成员之一
    membero(x, (2, 3, 4)))  # x is a member of (2, 3, 4) #x是（2,3,4）的成员之一


def logical_variable_expression():
    z = var('test')
    a, b, c = vars(3)
    print(repr(z), repr(a), repr(b), repr(c))


# Representing Knowledge
def store_data_as_facts():
    x = var()
    print(run(1, x, eq(x, 5)))
    parent = Relation()
    facts(parent, ("Homer", "Bart"),
                   ("Homer", "Lisa"),
                  ("Abe",  "Homer"))
    # who is Bart's father
    run(1, x, parent(x, "Bart"))

    # who is Homer's son
    run(2, x, parent("Homer", x))

    # who is Bart's grandfather
    y = var()
    run(1, x, parent(x, y), parent(y, 'Bart'))

# use conde, a goal constructor for logical and and or
def conde_logical_constructor():
    def grandparent(x, z):
        parent = Relation()
        y = var()
        return conde((parent(x, y), parent(y, z)))
    x = var()
    run(1, x, grandparent(x, 'Bart'))


def solve_who_owns_zebra():
    houses = var()

    def left(q, p, list):
        return membero((q, p), zip(list, list[1:]))

    def next(q, p, list):
        return conde([left(q, p, list)], [left(p, q, list)])

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
        
        (membero, (var(), var(), var(), 'zebra', var()), houses),  # 有人养斑马
        (membero, (var(), var(), 'water', var(), var()), houses)  # 有人喝水
        
    )
    
    solutions = run(0, houses, rules_zebraproblem)
    output_zebra = [house for house in solutions[0] if 'zebra' in house][0][0]
    print (output_zebra)

def measure_time(f):
    s = time.perf_counter()
    f()
    e = time.perf_counter()
    elapsed_time = e - s
    print(f"elapsed time: {elapsed_time:.4f} secs")


if __name__ == '__main__':
    measure_time(solve_who_owns_zebra)
