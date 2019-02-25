# coding=utf-8
import re, collections

# 拼写检查器

def words(text):
    # 只筛选出字母，将所有的字母会变成小写,变成一个个单词了
    return re.findall('[a-z]+', text.lower())

def train(features):
    # 遇到新的单词，设置词频默认为1（表示很小的概率）
    model = collections.defaultdict(lambda: 1)

    for f in features:
        model[f] += 1
    return model

# 导入语料库库文件，返回一个字典，字典键是单词，值是单词出现次数
NWORDS = train(words(open('big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    # 返回所有与单词w编辑距离为1的集合
    splits = []
    # 将单词分割成a,b
    for i in range(len(word)+1):
        # 长度是需要加一，在取最后一个的时候，是[4:4]
        splits.append((word[:i], word[i:]))
    # b多写1距离的可能性
    deletes = [a + b[1:] for a, b in splits if b]
    # b左右写错1距离的可能性
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    # b的第一个单词写错的可能性
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    # a 和b 中间少一个词的可能性
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    # 设置编辑距离等于2的集合，是在一的基础上
    # 优化：在这些编辑距离小于2的词中间，只把那些正确单词作为候选词
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

#正常来说把一个元音拼成另一个的概率要大于辅音，把单词第一个词拼错的概率小
# ，~~~但是，如果把这些都计算进去太复杂了，这里简化处理
# 设置编辑距离为1的正确单词比编辑距离为2的优先级高，而编辑距离为0的优先级比1高
# 0>1>2

# 所有单词的可能性
# 1：b多写一个词的可能性
# 2：b少写一个词的可能性
# 3：b的第一个单词写错的可能性
# 4：b左右写错1距离的可能性
def known(words):
    list1 = []
    for w in words:
        if w in NWORDS:
            list1.append(w)
    return list1

# 如果known(set)非空，candidates就会选择这个集合，而不再继续计算
def correct(word):
    # 优先级前面的满足就返回优先级高的单词
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    # 取出其中次数最大的值
    return max(candidates, key=NWORDS.get)

# 传入需要检查的单词
data = correct('lates')
print(data)