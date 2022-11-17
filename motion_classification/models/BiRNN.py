import sys

import torch
from torch import nn


class BiRNN(nn.Module):
    def __init__(self, vocab_size, embed_size, num_hiddens, num_layers, prob=0.5):
        """
        @params:
            vocab_size: 词典大小
            embed_size: 嵌入维度大小
            num_hiddens: 隐藏状态维度大小
            num_layers: 隐藏层个数
        """
        super(BiRNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)  # 映射长度,这里是降维度的作用

        # encoder-decoder framework
        # bidirectional设为True即得到双向循环神经网络
        self.encoder = nn.LSTM(input_size=embed_size,
                               hidden_size=num_hiddens,
                               num_layers=num_layers,
                               bidirectional=True)  # 双向循环网络
        self.dropout = nn.Dropout(prob)  # 随机丢弃一定比例的输入
        self.decoder = nn.Linear(4 * num_hiddens, 2)  # 初始时间步和最终时间步的隐藏状态作为全连接层输入

    def forward(self, inputs):
        """
        @params:
            inputs: 词语下标序列，形状为 (batch_size, seq_len) 的整数张量
        @return:
            outs: 对文本情感的预测，形状为 (batch_size, 2) 的张量
        """
        # 因为LSTM需要将序列长度(seq_len)作为第一维，所以需要将输入转置,注意这里转置了!!!!
        embeddings = self.embedding(inputs.permute(1, 0))  # (seq_len, batch_size, d)
        # print(embeddings.shape)
        # rnn.LSTM 返回输出、隐藏状态和记忆单元，格式如 outputs, (h, c)
        outputs, _ = self.encoder(embeddings)  # (seq_len, batch_size, 2*h)  每一个输出,然后将第一次输出和最后一次输出拼接
        # print(outputs.shape)# 如果是双向LSTM，每个time step的输出h = [h正向, h逆向] (同一个time step的正向和逆向的h连接起来)
        outputs = self.dropout(outputs)
        encoding = torch.cat((outputs[0], outputs[-1]), -1)  # (batch_size, 4*h)
        outs = self.decoder(encoding)  # (batch_size, 2)
        return outs


def test(argv):
    vocab_size, embed_size, num_hiddens, num_layers = 5000, 100, 100, 2
    net = BiRNN(vocab_size, embed_size, num_hiddens, num_layers)
    print(net)


if __name__ == '__main__':
    test(sys.argv)
