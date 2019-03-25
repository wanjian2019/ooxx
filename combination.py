import itertools

list1 = [1, 2, 3, 4]


print('没有顺利：', list(itertools.combinations(list1, 2)))
# print('没有顺利的组合：', list(itertools.combinations('12345', 4)))

print('有顺利：', list(itertools.permutations(list1, 2)))
# print('有顺利的全排列：', list(permutations('12345')))

print('有放回的抽样排列：', list(itertools.product(list1, repeat=2)))


print('OOXX排列：', list(itertools.product('OX', repeat=4)))


'''
>> from scipy.special import comb, perm
>> perm(3, 2)
6.0
>> comb(3, 2)
3.0
'''



