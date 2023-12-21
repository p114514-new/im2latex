from nltk.translate.bleu_score import sentence_bleu
import os
import distance

bleu_score = 0.0

hyp_path = r'I:\tempfiles\output\output\\'
hyp_path2 = r'I:\tempfiles\output_pure_mix\output1\\'
ref_path = r'I:\tempfiles\label1\labels_ds1\\'
ref_name_list = os.listdir(ref_path)
hyp_name_list = os.listdir(hyp_path)
hyp_name_list2 = os.listdir(hyp_path2)
hypotheses_t = []
hypotheses_t2 = []
references_t = []
references = []
hypotheses = []
hypotheses2 = []

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
    label_file_name2 = hyp_path2 + label_name
    with open(label_file_name2, 'r', encoding='utf-8') as f2:
        if label_file_name.endswith('.txt'):
            line = f2.read()
            hypotheses_t2.append(line)

for line in hypotheses_t:
    line = line.replace(" ", "")
    hypotheses.append(line)
for line in hypotheses_t2:
    line = line.replace(" ", "")
    hypotheses2.append(line)
for line in references_t:
    line = line.replace(" ", "")
    references.append(line)

label_names_with_chinese = []
# extract the label names of labels that contain chinese characters
for label_name in references:
    for char in label_name:
        if '\u4e00' <= char <= '\u9fa5':
            label_names_with_chinese.append(label_name)
            break

count1 = count2 = 0
for i in range(0, len(references)):
    if (references[i] == hypotheses[i] and references[i] != hypotheses2[i] and
            references[i] not in label_names_with_chinese):
        # print('ground truth: ', references[i])
        # print('pure model hypotheses: ', hypotheses[i])
        # print('mixed model hypotheses: ', hypotheses2[i])
        # print()
        count1 += 1
    if (references[i] == hypotheses2[i] and references[i] != hypotheses[i]
            and references[i] not in label_names_with_chinese):
        count2 += 1
print("pure model correct but mixed wrong: ", count1)
print("mixed model correct but pure wrong: ", count2)
