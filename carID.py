import cv2
import numpy as np
import os


def compare_image(src, dir):
    """
    从模板文件夹中遍历模板依次进行匹配，找到匹配度最高的模板，返回模板名称
    :param src:输入图像
    :param dir:匹配目录
    :return:返回最佳匹配模板的文件名
    """
    scores = []  # 匹配得分数组
    filenames = os.listdir(dir)
    for filename in os.listdir(dir):
        img = cv2.imread(dir + '/' + filename)
        imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 匹配和解析
        rv = cv2.matchTemplate(src, imggray, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(rv)
        # 记录每次匹配的最大值
        scores.append(maxVal)
    # 找到匹配度最大的模板名称
    maxvalue = max(scores)
    indexvalue = scores.index(maxvalue)
    return os.path.splitext(filenames[indexvalue])[0]


def findYAndX(src):
    """
    找到二值图像剪切的高度范围和宽度范围
    :param src:二值图像
    :return:高度范围和宽度范围
    """
    ystart, yend, xstart, xend = (0, 0, 0, 0)
    y, x = src.shape
    for i in range(0, x):
        for j in range(0, y):
            if src[j, i] > 0:
                if ystart <= 0:
                    ystart = j
                    break
                if j < ystart:
                    ystart = j
                    break

    for i in range(0, x):
        for j in range(y - 1, -1, -1):
            if src[j, i] > 0:
                if yend <= 0:
                    yend = j
                    break
                if j >= yend:
                    yend = j
                    break

    for j in range(0, y):
        for i in range(0, x):
            if src[j, i] > 0:
                if xstart <= 0:
                    xstart = i
                    break
                if i < xstart:
                    xstart = i
                    break

    for j in range(0, y):
        for i in range(x - 1, -1, -1):
            if src[j, i] > 0:
                if xend <= 0:
                    xend = i
                    break
                if i >= xend:
                    xend = i
                    break
    # 截取车牌区域
    return (ystart, yend, xstart, xend)


def findCarLoc(src):
    """
    车牌定位
    :param src:输入车牌图像
    :return:返回记录车牌位置的掩模
    """
    # 模板识别车牌区域
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # 将BGR图转成HSV图

    lower_blue = np.array([100, 43, 46])  # 能识别的最小的蓝色
    upper_blue = np.array([120, 255, 255])  # 能识别的最大蓝色
    mask = cv2.inRange(hsv, lower_blue, upper_blue)  # 设置hsv的颜色范围
    cv2.imshow("mask", mask)
    # 形态学去除周围的噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
    return opened


def cutCarImge(src, mask):
    """
    车牌切割
    :param src: 输入图像
    :param mask: 车牌区域掩模
    :return: 车牌图像
    """
    ystart, yend, xstart, xend = findYAndX(mask)
    dstim = src[ystart:yend, xstart:xend]
    return dstim


def cutCharImage(src):
    """
    字符切割
    :param src:输入图像
    :return:字符图像
    """
    # 调整尺寸
    src = cv2.resize(src, (196, 60))
    # 转换为灰度图
    dis = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # 阈值分割
    t, rst = cv2.threshold(dis, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary", rst)
    # 字符切割
    im0 = rst[10:50, 6:30]
    im1 = rst[10:50, 30:54]
    im2 = rst[10:50, 67:91]
    im3 = rst[10:50, 91:115]
    im4 = rst[10:50, 115:139]
    im5 = rst[10:50, 139:166]
    im6 = rst[10:50, 166:190]

    im0 = cv2.resize(im0, (20, 40))
    im1 = cv2.resize(im1, (20, 40))
    im2 = cv2.resize(im2, (20, 40))
    im3 = cv2.resize(im3, (20, 40))
    im4 = cv2.resize(im4, (20, 40))
    im5 = cv2.resize(im5, (20, 40))
    im6 = cv2.resize(im6, (20, 40))
    return (im0, im1, im2, im3, im4, im5, im6)


# 车牌识别车牌识别任务的实现过程有输入图像、预处理、车牌定位、字符分割、字符识别、输出结果等环节。重点关注：
# 1 车牌字符模板图像已经保存在dataset文件夹中，该方法对末班图像的要求比较高
# 2 本方法适用的车牌图像要求没有过多蓝色系的杂色，否则会影响识别效果
def carID(imgsrc):
    src = cv2.imread(imgsrc)
    cv2.imshow("input", src)
    # 车牌定位
    opened = findCarLoc(src)
    cv2.imshow("opened", opened)
    # 车牌剪切
    dstim = cutCarImge(src, opened)
    cv2.imshow("cut", dstim)
    # 字符剪切
    im0, im1, im2, im3, im4, im5, im6 = cutCharImage(dstim)
    cv2.imshow("0", im0)
    cv2.imshow("1", im1)
    cv2.imshow("2", im2)
    cv2.imshow("3", im3)
    cv2.imshow("4", im4)
    cv2.imshow("5", im5)
    cv2.imshow("6", im6)
    # 字符识别：模板匹配,所有模板都存放于dataset文件夹中
    carNumber = ''
    for im in [im0, im1, im2, im3, im4, im5, im6]:
        rs = compare_image(im, "dataset")
        carNumber += rs
    print(carNumber)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
