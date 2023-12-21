import json
from collections import Counter

with open(r'J:\github\image-to-latex\image_to_latex\data\vocab.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)
    print(len(vocab))
    vocab_keys = list(vocab.keys())

word = Counter()
with open(r'J:\github\image-to-latex\data\hunhe\im2latex_formulas.norm.new.lst','r', encoding='utf-8') as f2:
    train_lst = f2.readlines()
    train_lst = [x.strip() for x in train_lst]
    train_lst = [x.rsplit(' ', 1)[0] for x in train_lst]
    for line in train_lst:
        word.update(line.split(' '))

valid_keys = [x for x in word.keys() if word[x] >= 3]

keys_not_in_vocab = [x for x in valid_keys if x not in vocab_keys]
print(keys_not_in_vocab)

# # get the keys in keys_not_in_vocab but are not chinese characters
# keys_not_in_vocab_not_chinese = [x for x in keys_not_in_vocab if u'\u4e00' <= x <= u'\u9fff']
# print(keys_not_in_vocab_not_chinese)

keys_not_in_vocab.remove('。')
keys_not_in_vocab.remove('《')
keys_not_in_vocab.remove('》')
keys_not_in_vocab.remove('（')
keys_not_in_vocab.remove('）')

# append the keys_not_in_vocab_not_chinese vocabs to vocab
for key in keys_not_in_vocab:
    vocab[key] = len(vocab)

with open(r'J:\github\image-to-latex\image_to_latex\data\vocab_mixed.json', 'w', encoding='utf-8') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=4)
