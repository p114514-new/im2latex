import numpy as np
import distance
from nltk.translate.bleu_score import sentence_bleu
from tqdm import tqdm
import os


def evaluate(references, hypotheses):
    # 用于在验证集上计算各种评价指标指导模型早停
    # Calculate scores
    bleu4 = 0.0
    filtered_r = []
    filtered_h = []
    for i, j in zip(references, hypotheses):
        if len(i) >= 4 and len(j) >= 4:
            filtered_r.append(i)
            filtered_h.append(j)
    references = filtered_r
    hypotheses = filtered_h
    # print(references, hypotheses, sep='\n')
    for i, j in zip(references, hypotheses):
        bleu4 += max(sentence_bleu([i], j), 0.01)
    bleu4 = bleu4 / len(references)
    bleu4 = bleu4 * 100
    Edit_Distance = edit_distance(references, hypotheses)
    Exact_Match = np.mean([1.0 if r == h else 0.0 for r, h in zip(references, hypotheses)]) * 100
    # print([1.0 if r==h else 0.0 for r,h in zip(references, hypotheses)])
    return bleu4, Edit_Distance, Exact_Match


def edit_distance(references, hypotheses):
    """Computes Levenshtein distance between two sequences.
    Args:
        references: list of list of token (one hypothesis)
        hypotheses: list of list of token (one hypothesis)
    Returns:
        1 - levenshtein distance: (higher is better, 1 is perfect)
    """
    # d_leven, len_tot = 0, 0
    result = 0.0
    for ref, hypo in zip(references, hypotheses):
        result += distance.levenshtein(ref, hypo) / float(max(len(ref), len(hypo)))
        # d_leven += distance.levenshtein(ref, hypo)
        # print(d_leven)
        # len_tot += float(max(len(ref), len(hypo)))
    return (1. - result / len(references)) * 100
    # return (1. - d_leven / len_tot)*100


summary_dict = {
    '1':  # task 1
        {
            # group_id: {}
        },
    '2':  # task 2
        {
            # group_id: {}
        }
}

summary_dir = './evaluate_summary/'

if not os.path.exists(summary_dir):
    os.makedirs(summary_dir)

for task in [1, 2]:
    pred_dir = 's1_t{}'.format(task)
    target_file_dir = 'labels_ds{}'.format(task)

    for g_id in os.listdir(pred_dir):
        # if not (task == 2 and g_id == '7'):
        # continue
        g_dir = os.path.join(pred_dir, g_id)
        pred_lst = []
        gt_lst = []
        for t_f in tqdm(os.listdir(target_file_dir)):
            with open(os.path.join(target_file_dir, t_f), 'r') as f:
                gt_line = f.readlines()[0]
                gt_line = gt_line.strip().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')
                f.close()
            if len(os.listdir(g_dir)) == 1:
                g_dir = os.path.join(g_dir, os.listdir(g_dir)[0])
            if t_f in os.listdir(g_dir):
                with open(os.path.join(g_dir, t_f), 'r') as f:
                    try:
                        pred_line = f.readlines()[0]
                        pred_line = pred_line.strip().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n',
                                                                                                                   '')
                    except Exception:
                        pred_line = ''
            else:
                pred_line = ''
            pred_lst.append(pred_line)
            gt_lst.append(gt_line)
        # print(pred_lst[:3], gt_lst[:3], sep='-----', end='\n')
        bleu4, Edit_Distance, Exact_Match = evaluate(pred_lst, gt_lst)
        print('%s : bleu4=%.4f; Edit_Distance=%.4f; Exact_Match=%.4f' % (
            str(g_id) + '_' + str(task), bleu4, Edit_Distance, Exact_Match))
        summary_dict[str(task)][str(g_id)] = {'bleu_score': bleu4, 'edit_distance_score': Edit_Distance,
                                              'exact_match': Exact_Match}
