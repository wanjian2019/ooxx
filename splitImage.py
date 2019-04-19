import os
from PIL import Image
import cv2
from ai import Searcher
import time


# 最简单的以灰度直方图作为相似比较的实现
def classify_gray_hist(image1, image2, size=(256, 256)):
    # 先计算直方图
    # 几个参数必须用方括号括起来
    # 这里直接用灰度图计算直方图，所以是使用第一个通道，
    # 也可以进行通道分离后，得到多个通道的直方图
    # bins 取为16
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def get_text_from_image(file):
    img = cv2.imread(file)
    img_o = cv2.imread('file/o.png')
    img_x = cv2.imread('file/x.png')
    img_b = cv2.imread('file/b.png')
    d1 = classify_gray_hist(img, img_o)
    d2 = classify_gray_hist(img, img_x)
    d3 = classify_gray_hist(img, img_b)
    # print(file, d1, d2, d3)
    mv = max(d1, d2, d3)
    if mv == d1:
        return 'O'
    if mv == d2:
        return 'X'
    if mv == d3:
        return '-'


def get_text(rownum, colnum, dstpath):
    result = ''
    for r in range(rownum):
        for c in range(colnum):
            file = dstpath + str(r + 1) + '_' + str(c + 1) + '.png'
            result = result + get_text_from_image(file)
            if c == colnum-1:
                result = result + '\r\n'
    # result = result + '\r\n'
    return result


def splitimage(src, rownum, colnum, dstpath):
    k = 10
    # if rownum > 10:
    #     k = 5
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割, 请稍候...')
        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]
        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth+k, r * rowheight+k, (c + 1) * colwidth-k, (r + 1) * rowheight-k)
                # print(box)
                img.crop(box).save(os.path.join(dstpath, str(r+1) + '_' + str(c+1) + '.' + ext))
                num = num + 1
        print('图片切割完毕，共生成 %s 张小图片。' % num)
    else:
        print('不合法的行列切割参数！')


if __name__ == '__main__':
    t1 = time.time()

    row = 14
    col = 10
    splitimage('file/14104.png', row, col, './file/split/')
    data = get_text(row, col, './file/split/')
    print(data)
    searcher = Searcher(col, row)
    searcher.search_text(data)

    '''
    row = 6
    col = 6
    splitimage('file/66.png', row, col, './file/split/')
    data = get_text(row, col, './file/split/')
    print(data)
    searcher = Searcher(col, row)
    searcher.search_text(data)

    row = 10
    col = 8
    splitimage('file/1008.png', row, col, './file/split/')
    data = get_text(row, col, './file/split/')
    print(data)
    searcher = Searcher(col, row)
    searcher.search_text(data)
    '''
    t2 = time.time()
    print('total second:', t2-t1)
