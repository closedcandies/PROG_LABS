from logger import *


@trace(handle=sys.stderr)  # @trace
def increm(x):
    """Инкремент"""
    return x + 1

@trace(handle=sys.stdout)
def decrem(x):
    """Декремент"""
    return x-1


print(increm.__doc__)
increm(2)
decrem(2)


@deco() # Default: Вариант по умолчанию
def f2(x):
    return x**2

import json
@deco(handle='logger.json') # Default: Вариант по умолчанию
def f3(x):
    return x**3

import sqlite3
handle_for_f4 = sqlite3.connect(":memory:")

@deco(handle=handle_for_f4) # Default: Вариант по умолчанию
def f4(x):
    return x**4


# NOTE: Возможно, здесь должен быть вызов f3 и f4...

showlogs(handle_for_f4)