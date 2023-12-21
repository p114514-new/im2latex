from image_to_latex.data.utils import Tokenizer

tokenizer = Tokenizer().load(r"J:\github\image-to-latex\image_to_latex\data\vocab_pure.json")
line = r'P ( a , b ) \text { . }'
line = line.split()
tokens = tokenizer.encode(line)
print(tokens)