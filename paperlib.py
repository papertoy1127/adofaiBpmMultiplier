
def append(item, *target):
    if len(target) > 1:
        raise TypeError('append() takes 2 positional argument but {} were given'.format(len(target) + 1))
    elif len(target) < 1:
        raise TypeError('append() missing 1 required positional argument: \'*target\'')
    target[0].append(item)
    return target[0]

#테스트코드
if __name__ == '__main__':
    a = 4
    b = [0, 1, 2, 3]
    print(append(a, b))
    print(b)