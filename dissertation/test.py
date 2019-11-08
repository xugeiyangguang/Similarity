from dissertation.cosine import cosine_similarity
from dissertation.tf_idf import weight_list
if __name__ == '__main__':

    print(cosine_similarity(weight_list[0].tolist(), weight_list[1].tolist()))
