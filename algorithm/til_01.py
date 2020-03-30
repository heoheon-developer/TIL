# 2019/02/25 오늘 공부

import math  # 수학모듈사용


# 절댓값 알고리즘 1(부호 판단)
# 입력 : 실수 a
# 출력 : a의 절댓값

def abs_sign(a):
    if a >= 0:
        return a
    else:
        return -a

def abs_square(a):
    b = a * a
    return math.sqrt(b)

print(abs_sign(5))
print(abs_sign(-3))
