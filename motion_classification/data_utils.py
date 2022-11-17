import collections
import os
import random
import sys
import jieba
import torch
import torch.utils.data as Data
import torchtext.vocab as vocab
from tqdm import tqdm


def read_review(tag='train', data_root="Data\\"):
    data = []
    input_file = os.path.join(data_root, "{0}.csv".format(tag))
    with open(input_file, 'r', encoding="utf8") as f:
        head_line = f.readline()
        for line in tqdm(f):
            line = line.strip()
            label = int(line[0])
            review = line[2:]
            data.append([review, label])  # 评论文本字符串和01标签
    random.shuffle(data)
    return data


def get_tokenized_review(data):  # 将每行数据的进行空格切割,保留每个的单词
    # 此处可以添加更复杂的过滤逻辑
    def tokenizer(text):
        return [tok for tok in jieba.cut(text)]

    return [tokenizer(review) for review, _ in data]


def get_vocab_review(data, min_count=1):
    """
    @params:
        data: 同上
    @return: 数据集上的词典，Vocab 的实例（freqs, stoi, itos）
    """
    tokenized_data = get_tokenized_review(data)
    counter = collections.Counter([tk for st in tokenized_data for tk in st])
    # 统计所有的数据
    dict = vocab.vocab(counter, min_freq=min_count)  # 构建词汇表
    # 加入<pad> 和 <unk>
    dict.insert_token("<pad>", 0)
    dict.insert_token("<unk>", 1)
    return dict


def preprocess_review(data, vocab, max_l=64):
    def pad(x):  # 填充
        return x[:max_l] if len(x) > max_l else x + [vocab["<pad>"]] * (max_l - len(x))

    tokenized_data = get_tokenized_review(data)
    padded_tokenized_data = []
    for words in tokenized_data:
        indexed_words = [vocab[word] if word in vocab else vocab["<unk>"] for word in words]
        padded_words = pad(indexed_words)
        padded_tokenized_data.append(padded_words)
    features = torch.tensor(padded_tokenized_data)
    labels = torch.tensor([score for _, score in data])
    return features, labels


def make_review_dataset(batch_size=64, max_length=64, min_count=5):
    # 读取文本数据
    train_data, test_data = read_review(tag="train"), read_review(tag="test")
    # 获取字典
    vocab = get_vocab_review(train_data, min_count)
    # *号语法糖,解绑参数，获取dataset对象
    train_set = Data.TensorDataset(*preprocess_review(train_data, vocab, max_length))
    test_set = Data.TensorDataset(*preprocess_review(test_data, vocab, max_length))  # 相当于将函数参数是函数结果
    # 获取迭代器
    train_iter = Data.DataLoader(train_set, batch_size, shuffle=True)
    test_iter = Data.DataLoader(test_set, batch_size)

    return train_iter, test_iter, vocab


def make_review_testset(file_path, vocab_path, batch_size=64, max_length=64):
    # 读取数据
    data = []
    with open(file_path, 'r', encoding="utf8") as f:
        for line in f:
            review = line.strip()
            label = 0  # 标签固定为0
            data.append([review, label])

    # 读入词典
    vocab = read_vocab(vocab_path)

    # *号语法糖,解绑参数，获取dataset对象
    data_set = Data.TensorDataset(*preprocess_review(data, vocab, max_length))  # 相当于将函数参数是函数结果
    # 获取迭代器
    data_iter = Data.DataLoader(data_set, batch_size)

    return data_iter, vocab


def save_vocab(vocab, path):
    # print(vocab.get_itos())
    with open(path, 'w', encoding="utf8") as output:
        print("\n".join(vocab.get_itos()), file=output)


def read_vocab(vocab_path):
    vocab_dict = {}
    with open(vocab_path, 'r', encoding="utf8") as f:
        for line in f:
            word = line[:-1]
            # print("*{0}*".format(word))
            if word == "":
                continue
            vocab_dict[word] = 1
    dict = vocab.vocab(vocab_dict, min_freq=0)

    return dict


def load_pretrained_embedding(words, pretrained_vocab_path=None, emb_size=100, type="glove"):
    """
    @params:
        words: 需要加载词向量的词语列表，以 itos (index to string) 的词典形式给出
        pretrained_vocab: 预训练词向量
        type: 词向量的种类
    @return:
        embed: 加载到的词向量
    """
    # embed = torch.zeros(len(words), emb_size)  # 初始化为len*100维度
    embed = torch.normal(mean=0, std=1, size=(len(words), emb_size))

    if type == "glove":
        # 先硬编码使用100d的glove向量
        pretrained_vocab = vocab.GloVe(name="6B", dim=100, cache="data\\glove")
    else:
        return embed

    pretrained_emb_size = pretrained_vocab.vectors[0].shape[0]
    oov_count = 0  # out of vocabulary
    for i, word in enumerate(words):
        try:
            idx = pretrained_vocab.stoi[word]
            if pretrained_emb_size == emb_size:
                embed[i, :] = pretrained_vocab.vectors[idx]  # 将每个词语用训练的语言模型理解
            elif pretrained_emb_size < emb_size:
                embed[1, :] = pretrained_vocab.vectors[idx] + [0] * (emb_size - pretrained_emb_size)
            else:
                embed[1, :] = pretrained_vocab.vectors[idx][:emb_size]
        except KeyError:
            oov_count += 1
    if oov_count > 0:
        print("There are %d oov words." % oov_count)
    # print(embed.shape),在词典中寻找相匹配的词向量
    return embed


def testread():
    train_data, test_data = read_review(tag="train"), read_review(tag="test")
    # 打印训练数据中的前五个sample
    for sample in train_data[:5]:
        print(sample[1], '\t', sample[0][:50])


def test(argv):
    train_iter, test_iter, _ = make_review_dataset(min_count=5)
    print('#train_batches:', len(train_iter))

    for X, y in train_iter:
        print('X', X, 'y', y)
        break
    print('#test_batches:', len(test_iter))
    for X, y in test_iter:
        print('X', X, 'y', y)
        break


if __name__ == '__main__':
    test(sys.argv)
