import glob
import numpy as np
import pandas as pd
import pickle
import random
import sys
from scipy.sparse import dok_matrix

file_name = "matrix.data"
shape_name = "shape.data"


def readData():
    files = glob.glob("./csv/*.csv")
    arrays = []
    for file in files:
        csv = pd.read_csv(file)
        arrays.append(csv.to_numpy())
    return arrays


def getShape(arrays):
    MAX_X = 0
    MAX_Y = 0
    for array in arrays:
        l = array.max(0)
        MAX_X = l[0] if l[0] > MAX_X else MAX_X
        MAX_Y = l[1] if l[1] > MAX_Y else MAX_Y
    return (MAX_X + 1, MAX_Y + 1)


def setM(arrays, M, shape):
    print("开始填充矩阵")
    size = len(arrays)
    n = 0
    for array in arrays:
        cur = array[0]
        for id in range(1, array.shape[0]):
            next = array[id]
            i = getIndex(shape, cur[0], cur[1])
            j = getIndex(shape, next[0], next[1])
            M[i, j] = M[i, j] + 1
            cur = next
        n = n + 1
        print("{:d}/{:d}".format(n, size))

    print("开始初始化maps")
    maps = {}
    n = 0
    size = len(M.keys())
    print(size)
    for xy in M.keys():
        x, y = xy[0], xy[1]
        if x in maps.keys():
            # 因为是遍历稀疏矩阵,y一定不在xmap[x]中,省去查重直接添加
            maps[x].append({y: M[x, y]})
            in_maps = True
        # x不在maps中时,maps中添加{x: [{y: M[x, y]}]}
        else:
            maps[x] = [{y: M[x, y]}]
        n = n + 1
        print("{:d}/{:d}".format(n, size))
    print("开始求行平均")
    n = 0
    size = len(maps)
    for x in maps.keys():
        ys = []
        row_sum = 0
        for ymap in maps[x]:
            if len(ymap.keys()) != 1:
                raise ValueError("错误的ymap key")
            y = list(ymap.keys())[0]
            ys.append(y)
            row_sum = row_sum + ymap[y]
        for y in ys:
            M[x, y] = M[x, y] / row_sum
        n = n + 1
        print("{:d}/{:d}".format(n, size))


def getIndex(shape, x, y):
    return x * shape[1] + y


def index2xy(shape, index):
    y = index % shape[1]
    x = index // shape[1]
    return (x,y)

def getRandomStart(M,shape):
    keys = M.keys()
    size = len(keys)
    index = random.randint(0, size)
    xy = list(keys)[index]
    x,y = index2xy(shape,xy[0])
    return x, y


def dumpData():
    arrays = readData()
    shape = getShape(arrays)
    len = shape[0] * shape[1]
    m = dok_matrix((len, len), np.float64)
    setM(arrays, m, shape)
    with open(file_name, "wb") as f:
        pickle.dump(m, f)
    with open(shape_name, "wb") as f:
        pickle.dump(shape, f)


def loadData():
    with open(file_name, "rb") as f:
        m = pickle.load(f)
    with open(shape_name, "rb") as f:
        shape = pickle.load(f)
    return m, shape


def run(steps=100):
    m, shape = loadData()
    # print(m)
    print(shape)
    start = getRandomStart(m,shape)
    print("起始位置:", start)
    size = shape[0] * shape[1]
    status = dok_matrix((1, size), dtype=np.float64)
    status[0, getIndex(shape, start[0], start[1])] = 1.0
    for i in range(steps):
        # 向量太大,超时
        # print(status)
        status = status * m
        # status = multiply(status, m)
        index = np.argmax(status)
        xy = index2xy(shape, index)
        print("第{:d}步位置  X:{:d} Y:{:d}".format(i + 1, xy[0], xy[1]))


def multiply(status, M):
    temp = dok_matrix(status.shape, np.float64)
    ys = {}
    for xy in M.keys():
        y = xy[1]
        if y not in ys.keys():
            ys[y] = None
    print(len(ys.keys()))
    n = 0
    for j in ys.keys():
        col = M[:, j]
        temp[0, j] = row_x_col(status, col)
        print(n)
        n = n + 1
    return temp


def row_x_col(row, col):
    sum = 0
    for xy in col.keys():
        x = xy[0]
        y = xy[1]
        if col[x, y] != 0:
            sum = sum + row[0, x] * col[x, 0]
    return sum


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "DumpData":
        dumpData()
    elif cmd == "Run":
        run()
