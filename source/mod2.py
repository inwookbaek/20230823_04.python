"""
    modul2 입니다!
"""
def add(a, b):
    return a+b

def safe_add(a, b):
    if type(a) != type(b):
        print(f'a({type(a)})와 b({type(b)})의 자료형이 다릅니다!')
        return
    else:
        result = add(a,b)
        return result

def sub(a, b):
    return a-b

def main():
    print(__name__)
    print(add(20, 10))
    print(safe_add(1, 'xxxx'))
    print(sub(20,10))

if __name__ == '__main__':
    main()
