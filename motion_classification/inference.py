# -*- coding:utf-8 -*-

import os
import sys
import time

import torch
from torch import nn

from models.BiRNN import BiRNN
from data_utils import make_review_testset, read_vocab

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def infer(data_iter, net, device):
    total_result = []
    net = net.to(device)
    print("inferencing on ", device)
    for X, _ in data_iter:
        net.eval()
        results = net(X.to(device)).argmax(dim=1)
        # 记录结果
        total_result.extend(results.cpu().numpy().tolist())
    return total_result


def main(argv):
    # 载入词典并读取推理用数据
    test_file_path = "../Data/reviewForInfer/review.csv"

    vocab_path = "output\\model.vocab"
    data_iter, vocab = make_review_testset(test_file_path, vocab_path)
    print("#vocab: ", len(vocab))
    print('#batches:', len(data_iter))

    # 载入模型
    model_path = "output\\model.pt"
    net = torch.load(model_path)
    print("#model:", net)

    # 开始推理
    res = infer(data_iter, net, device)
    # print("#results : ", res)

    # 保存结果
    with open("../Data/reviewForInfer/result.csv", "w") as f:
        for r in res:
            f.write(str(r) + "\n")


if __name__ == '__main__':
    main(sys.argv)
