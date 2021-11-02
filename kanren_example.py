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


def solve_zebra_problem():
    """
    有五间房子。
    英国人住在红房子里。
    瑞典人有一只狗。
    丹麦人喝茶。
    绿房子在白房子的左边。
    他们在绿房子里喝咖啡。
    吸Pall Mall的人有鸟。
    吸Dunhill在的人黄色房子里。
    在中间的房子里，他们喝牛奶。
    挪威人住在第一宫。
    那个抽Blend的男人住在猫屋旁边的房子里。
    在他们有一匹马的房子旁边的房子里，他们吸Dunhill烟。
    抽Blue Master的人喝啤酒。
    德国人吸Prince烟。
    挪威人住在蓝房子旁边。
    他们在房子旁边的房子里喝水，在那里吸Blend烟。
    :return:
    """
    houses = var()

    def left(q, p, list):
        return membero((q, p), zip(list, list[1:]))

    def next(q, p, list):
        return conde([left(q, p, list)], [left(p, q, list)])

    rules_zebraproblem = lall(
        (eq, (var(), var(), var(), var(), var()), houses),  # 5个var（）分别代表 人、烟、饮料、动物、屋子颜色
        (membero, ('Englishman', var(), var(), var(), 'red'), houses),
        (membero, ('Swede', var(), var(), 'dog', var()), houses),
        (membero, ('Dane', var(), 'tea', var(), var()), houses),
        (left, (var(), var(), var(), var(), 'green'),
         (var(), var(), var(), var(), 'white'), houses),
        (membero, (var(), var(), 'coffee', var(), 'green'), houses),
        (membero, (var(), 'Pall Mall', var(), 'birds', var()), houses),
        (membero, (var(), 'Dunhill', var(), var(), 'yellow'), houses),
        (eq, (var(), var(), (var(), var(), 'milk', var(), var()), var(), var()), houses),
        (eq, (('Norwegian', var(), var(), var(), var()), var(), var(), var(), var()), houses),
        (next, (var(), 'Blend', var(), var(), var()),
         (var(), var(), var(), 'cats', var()), houses),
        (next, (var(), 'Dunhill', var(), var(), var()),
         (var(), var(), var(), 'horse', var()), houses),
        (membero, (var(), 'Blue Master', 'beer', var(), var()), houses),
        (membero, ('German', 'Prince', var(), var(), var()), houses),
        (next, ('Norwegian', var(), var(), var(), var()),
         (var(), var(), var(), var(), 'blue'), houses),
        (next, (var(), 'Blend', var(), var(), var()),
         (var(), var(), 'water', var(), var()), houses),
        (membero, (var(), var(), var(), 'zebra', var()), houses)
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
    measure_time(solve_zebra_problem)
