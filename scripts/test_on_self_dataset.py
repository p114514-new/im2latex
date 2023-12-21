import os

import numpy as np
import torch
from albumentations.pytorch.transforms import ToTensorV2
from PIL import Image
from tqdm import tqdm
from torchvision import transforms
from image_to_latex.lit_models import LitResNetTransformer


lit_model = LitResNetTransformer.load_from_checkpoint(
    r"I:\tempfiles\cer")

lit_model.freeze()
transform = ToTensorV2()
file_path = r"J:\github\image-to-latex\test_images"
file = os.listdir(file_path)

for i in tqdm(range(len(file))):
    img_name = file[i]
    img_path = f'J:/github/image-to-latex/test_images/{img_name}'
    image = Image.open(img_path).convert("L")
    image_tensor = transform(image=np.array(image))["image"]
    # toPIL=transforms.ToPILImage()
    # pic=toPIL(image_tensor)
    # pic.show()
    # print(image_tensor)# type: ignore
    pred = lit_model.model.predict(image_tensor.unsqueeze(0).float())[0]  # type: ignore
    decoded = lit_model.tokenizer.decode(pred.tolist())  # type: ignore
    decoded_str = " ".join(decoded)
    with open(r"J:/github/image-to-latex\data\latex.txt", 'a', encoding='utf-8') as f:
        f.write(img_name + ": ")
        f.write(decoded_str)
        f.write('\n')