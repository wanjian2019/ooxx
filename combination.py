import itertools

list1 = [1, 2, 3, 4]


print('没有顺序：', list(itertools.combinations(list1, 2)))
# print('没有顺序的组合：', list(itertools.combinations('12345', 4)))

print('有顺序：', list(itertools.permutations(list1, 2)))

print('有顺序：', list(itertools.permutations(list1)))

listA = list(itertools.permutations('ABCD'))
print('有顺序的全排列：', len(listA), listA)

print('有放回的抽样排列：', list(itertools.product(list1, repeat=2)))


print('OOXX排列：', list(itertools.product('OX', repeat=4)))


'''
>> from scipy.special import comb, perm
>> perm(3, 2)
6.0
>> comb(3, 2)
3.0
'''



