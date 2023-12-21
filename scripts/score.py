import numpy as np
from nltk.translate.bleu_score import sentence_bleu
import os
import distance

hyp_path = r'I:\tempfiles\output_trans_\output_trans_\\'
ref_path = r'I:\tempfiles\label1\labels_ds1\\'

# hyp_path = r'I:\tempfiles\output2\output2\output2\\'
# ref_path = r'I:\tempfiles\label2\labels_ds2\\'

ref_name_list = os.listdir(ref_path)
hyp_name_list = os.listdir(hyp_path)
hypotheses_t = []
references_t = []
references = []
hypotheses = []
for label_name in ref_name_list:
    # use the name of the label file to find the corresponding hypothesis file
    label_file_name = ref_path + label_name
    with open(label_file_name, 'r', encoding='utf-8') as f1:
        if label_file_name.endswith('.txt'):
            line = f1.read()
            references_t.append(line)
    label_file_name1 = hyp_path + label_name
    with open(label_file_name1, 'r', encoding='utf-8') as f2:
        if label_file_name.endswith('.txt'):
            line = f2.read()
            hypotheses_t.append(line)

for line in hypotheses_t:
    line = line.strip().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')
    hypotheses.append(line)
for line in references_t:
    try:
        line = line.strip().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')
        references.append(line)
    except:
        print(1)
        references.append('')


def evaluate():
    global references, hypotheses
    # 用于在验证集上计算各种评价指标指导模型早停
    # Calculate scores
    bleu4 = 0.0
    filtered_r = []
    filtered_h = []
    count = 0
    for i, j in zip(references, hypotheses):
        if len(i) >= 4 and len(j) >= 4:
            filtered_r.append(i)
            filtered_h.append(j)
        else:
            count += 1
    print(count)
    print(len(filtered_r))
    references = filtered_r
    hypotheses = filtered_h
    # print(references, hypotheses, sep='\n')
    for i, j in zip(references, hypotheses):
        bleu4 += max(sentence_bleu([i], j), 0.01)
    bleu4 = bleu4 / len(references)
    bleu4 = bleu4 * 100
    Edit_Distance = edit_distance(references, hypotheses)
    Exact_Match = np.mean([1.0 if r == h else 0.0 for r, h in zip(references, hypotheses)]) * 100
    # for r, h in zip(references, hypotheses):
    #     if r != h:
    #         print(r)
    #         print(h)
    return bleu4, Edit_Distance, Exact_Match


def edit_distance(references, hypotheses):
    """Computes Levenshtein distance between two sequences.
    Args:
        references: list of list of token (one hypothesis)
        hypotheses: list of list of token (one hypothesis)
    Returns:
        1 - levenshtein distance: (higher is better, 1 is perfect)
    """
    result = 0.0
    for ref, hypo in zip(references, hypotheses):
        result += distance.levenshtein(ref, hypo) / float(max(len(ref), len(hypo)))
    return (1. - result / len(references)) * 100


bleu4, Edit_Distance, Exact_Match = evaluate()
print('%s : bleu4=%.4f; Edit_Distance=%.4f; Exact_Match=%.4f' % (
    "group5_task1", bleu4, Edit_Distance, Exact_Match))
