import os
import re

pure_dir = r'I:\tempfiles\output\output\\'
mixed_dir = r'I:\tempfiles\output_pure_mix\output1\\'

pure_list = os.listdir(pure_dir)
mixed_list = os.listdir(mixed_dir)
hyp_pure = {}
hyp_mixed = {}

for label_name in pure_list:
    # use the name of the label file to find the corresponding hypothesis file
    label_file_name = pure_dir + label_name
    with open(label_file_name, 'r', encoding='utf-8') as f1:
        if label_file_name.endswith('.txt'):
            line = f1.read()
            hyp_pure[label_name] = line

for label_name in mixed_list:
    # use the name of the label file to find the corresponding hypothesis file
    label_file_name = mixed_dir + label_name
    with open(label_file_name, 'r', encoding='utf-8') as f1:
        if label_file_name.endswith('.txt'):
            line = f1.read()
            hyp_mixed[label_name] = line

label_names_with_chinese = []
# extract the label names of labels that contain chinese characters
for label_name in hyp_mixed.keys():
    for char in hyp_mixed[label_name]:
        if '\u4e00' <= char <= '\u9fa5':
            label_names_with_chinese.append(label_name)
            break


def align_labels(non_chinese_label, chinese_label):
    # Extract \text{} sequences from the non-chinese label
    non_chinese_sequences = re.findall(r'\\text \{(.*?)}', non_chinese_label)

    # Extract \text{} sequences and their contents from the Chinese label
    chinese_sequences = re.findall(r'\\text \{ (.*?)}', chinese_label)
    # Make sure the number of Chinese sequences is not greater than non-Chinese sequences
    chinese_sequences = chinese_sequences[:len(non_chinese_sequences)]

    # Insert the contents of the Chinese \text{} sequences into the corresponding non-Chinese \text{} sequences
    aligned_label = non_chinese_label
    for chinese_seq, non_chinese_seq in zip(chinese_sequences, non_chinese_sequences):
        aligned_label = aligned_label.replace(f'\\text {{{non_chinese_seq}}}',
                                              f'\\text{{{non_chinese_seq}{chinese_seq}}}', 1)

    return aligned_label


for label_name in label_names_with_chinese:
    hyp_pure[label_name] = align_labels(hyp_pure[label_name], hyp_mixed[label_name])

output_dir = r'I:\tempfiles\output_trans'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# output the aligned labels into separate txt files
for label_name in hyp_pure.keys():
    with open(output_dir + '\\' + label_name, 'w', encoding='utf-8') as f:
        f.write(hyp_pure[label_name])
