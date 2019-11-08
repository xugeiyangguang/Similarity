import numpy as np


def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    # dot_product, square_sum_x, square_sum_y = 0, 0, 0
    # for i in range(len(x)):
    #     dot_product += x[i] * y[i]
    #     square_sum_x += x[i] * x[i]
    #     square_sum_y += y[i] * y[i]
    # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内


if __name__ == '__main__':

    print("余弦相似度的最终结果：")
    print(cosine_similarity([0, 0], [0, 0]))  # 1.0
    print(cosine_similarity([1, 1], [0, 0]))  # 0.0
    print(cosine_similarity([1, 1], [-1, -1]))  # -1.0
    print(cosine_similarity([1, 1], [2, 2]))  # 1.0
    print(cosine_similarity([1, 1, 2, 1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 1, 1, 1, 1, 1]))  # 1.0
    print(cosine_similarity([1, 2, 2, 1, 1, 1, 0], [1, 2, 2, 1, 1, 2, 1]))  # 0.938194187433