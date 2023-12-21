import os
import re

pure_dir = r'I:\tempfiles\output2\output2\output2\\'

pure_list = os.listdir(pure_dir)

for label_name in pure_list:
    # use the name of the label file to find the corresponding hypothesis file
    label_file_name = pure_dir + label_name
    with open(label_file_name, 'r', encoding='utf-8') as f1:
        if label_file_name.endswith('.txt'):
            line = f1.read()
            line = line.replace(r'\leq s l a n t', r'\leqslant')

    with open(label_file_name, 'w', encoding='utf-8') as f2:
        f2.write(line)