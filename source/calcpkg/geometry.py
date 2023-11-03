def triangle_area(width, height):
    return width * height / 2

def rectangle_area(width, height):
    return width * height

def main():
    print(f'삼각형의 넓이 = {triangle_area(10, 10)}')
    print(f'사각형의 넓이 = {rectangle_area(10, 10)}')
    
if __name__ == '__main__':
    main()