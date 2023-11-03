def add(a, b):
    return a+b

def safe_add(a, b):
    if type(a) != type(b):
        print(f'a({type(a)})와 b({type(b)})의 자료형이 다릅니다!')
        return
    else:
        result = add(a,b)
        return result
