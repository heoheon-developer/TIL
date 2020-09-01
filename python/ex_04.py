# 직접 해보는 손코딩
# 범위 내부의 정수를 모두 더하는 함수

# 함수 선언

def sum_all(start, end):
    #변수 선언
    output = 0
    #반복문을 돌려 숫자를 더함

    for i in range(start, end + 1):
        output += i
    #리턴
    return output

#함수 호출

print("0 to 100 :", sum_all(0, 100))
print("0 to 1000 :", sum_all(0, 1000))
print("50 to 100 :", sum_all(50, 100))
print("500 to 1000 :", sum_all(500, 1000))