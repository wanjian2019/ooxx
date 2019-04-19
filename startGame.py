#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ai import Searcher
import time

if __name__ == '__main__':
    data = [[] for i in range(30)]
    print('输入初始棋谱：')
    stopword = ''
    i = 0
    width = 0
    for line in iter(input, stopword):
        for t2 in line:
            data[i].append(t2)
        i = i + 1
        width = len(line)

    t1 = time.time()
    print(width, i)
    searcher = Searcher(width, i)
    searcher.search(data)
    t2 = time.time()
    print('total second:', t2-t1)
