import itertools

'''
1、输入得到四个数
2、生成四个数的全排列
3、生成+-*/的全排列
4、两个组合，生成公式
5、计算结果，等于24，ok
6、括号情况加上去
'''
TF_24 = 24


def _all_combination(list4):
    return list(itertools.permutations(list4))


def _all_combination_char(a1, a2, a3, a4):
    return list(itertools.product((a1, a2, a3, a4), repeat=3))


def _calculate(num_list, char_list):
    """
    a1+a2*a3-a4

    (a1+a2)*a3-a4
    a1+(a2*a3)-a4
    a1+a2*(a3-a4)

    (a1+a2*a3)-a4
    a1+(a2*a3-a4)

    (a1+a2)*(a3-a4)
    a1+((a2*a3)-a4)
    ((a1+a2)*a3)-a4
    """
    found = False
    for arr1 in num_list:
        a1 = arr1[0]
        a2 = arr1[1]
        a3 = arr1[2]
        a4 = arr1[3]
        for arr2 in char_list:
            c1 = arr2[0]
            c2 = arr2[1]
            c3 = arr2[2]
            if _join(a1, c1, a2, c2, a3, c3, a4) \
                    or _join('(', a1, c1, a2, ')', c2, a3, c3, a4) \
                    or _join(a1, c1, '(',  a2, c2, a3, ')', c3, a4) \
                    or _join(a1, c1, a2, c2, '(', a3, c3, a4, ')') \
                    or _join('(', a1, c1, a2, c2, a3, ')', c3, a4) \
                    or _join(a1, c1, '(', a2, c2, a3, c3, a4, ')') \
                    or _join('(', a1, c1, a2, ')', c2, '(', a3, c3, a4, ')') \
                    or _join(a1, c1, '((', a2, c2, a3, ')', c3, a4, ')') \
                    or _join('((', a1, c1, a2, ')', c2, a3, ')', c3, a4):
                found = True
    if not found:
        print('没找到匹配的结果，无解')


def _join(*args):
    result = ''
    for arg in args:
        result += arg
    try:
        if eval(result) == TF_24:
            print(result)
            return True
    except ZeroDivisionError as e:
        pass
    return False


if __name__ == '__main__':
    '''
    print(eval('1+1+1*9'))
    print(eval('3-1*1-9'))
    print(eval('1*8-1*9'))
    '''
    init = []
    stop = ''
    i = 0
    for line in iter(input, stop):
        if line.isdigit():
            init.append(line)
            i += 1
        if i >= 4:
            break
    num_list = _all_combination(init)
    char_list = _all_combination_char('+', '-', '*', '/')
    _calculate(num_list, char_list)
