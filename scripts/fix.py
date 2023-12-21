import os

folder = r"I:\tempfiles\label1\images_new"

# find all txt files in the folder
file_list = os.listdir(folder)

# loop through all txt files
# for each txt file, find sequences that keep repeating
# for each sequence of this kind, keep only 3 copies
count = 0
for file in file_list:
    count += 1
    file_path = os.path.join(folder, file)
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.read()
        words = line.split(' ')
        i = 0
        # find one word that keeps repeating
        while i < len(words):
            word = words[i]
            j = i + 1
            while j < len(words) and words[j] == word:
                j += 1
            # if there are more than 3 copies, keep only 3 copies
            if j - i > 3:
                words = words[:i] + [word] * 3 + words[j:]
            i += 1

        # find two adjacent words that keep repeating
        i = 0
        while i < len(words) - 1:
            word1 = words[i]
            word2 = words[i + 1]
            j = i + 2
            while j < len(words) - 1 and words[j] == word1 and words[j + 1] == word2:
                j += 2
            # if there are more than 3 copies, keep only 3 copies
            if j - i > 3:
                words = words[:i] + [word1, word2] * 3 + words[j:]
            i += 1

        # find three adjacent words that keep repeating
        i = 0
        while i < len(words) - 2:
            word1 = words[i]
            word2 = words[i + 1]
            word3 = words[i + 2]
            j = i + 3
            while j < len(words) - 2 and words[j] == word1 and words[j + 1] == word2 and words[j + 2] == word3:
                j += 3
            # if there are more than 3 copies, keep only 3 copies
            if j - i > 3:
                words = words[:i] + [word1, word2, word3] * 3 + words[j:]
            i += 1

        # output the processed txt file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(' '.join(words))