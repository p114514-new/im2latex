import os
import random

import numpy as np
import torch
from albumentations.pytorch.transforms import ToTensorV2
from PIL import Image
from tqdm import tqdm
from torchvision import transforms
from image_to_latex.lit_models import LitResNetTransformer

lit_model = LitResNetTransformer.load_from_checkpoint(
    r"J:\github\image-to-latex\scripts\outputs\2023-12-12\22-48-32\lightning_logs\version_0\checkpoints\epoch=17-val\loss=0.09-val\cer=0.03.ckpt")

lit_model.freeze()
transform = ToTensorV2()
file_path = r"I:\tempfiles\label1\images1_processed"
file = os.listdir(file_path)

output_path = r"I:\tempfiles\label1\images_test_using_mixed"
if not os.path.exists(output_path):
    os.makedirs(output_path)

# for i in tqdm(range(len(file))):
#     img_name = file[i]
#     img_path = os.path.join(file_path, img_name)
#     image = Image.open(img_path).convert("L")
#     image_tensor = transform(image=np.array(image))["image"]
#     pred = lit_model.model.predict(image_tensor.unsqueeze(0).float())[0]  # type: ignore
#     decoded = lit_model.tokenizer.decode(pred.tolist())  # type: ignore
#     decoded_str = " ".join(decoded)
#     with open(os.path.join(output_path, img_name[:-4] + '.txt'), 'a', encoding='utf-8') as f:
#         f.write(decoded_str)


def collate_fn(images):
    B = len(images)
    max_H = max(image.shape[1] for image in images)
    max_W = max(image.shape[2] for image in images)
    padded_images = torch.zeros((B, 1, max_H, max_W))
    for i in range(B):
        H, W = images[i].shape[1], images[i].shape[2]
        y, x = random.randint(0, max_H - H), random.randint(0, max_W - W)
        padded_images[i, :, y : y + H, x : x + W] = images[i]
    return padded_images

images = []
image_names = []
# read in all images and store them in a list
for i in tqdm(range(len(file))):
    img_name = file[i]
    img_path = os.path.join(file_path, img_name)
    image = Image.open(img_path).convert("L")
    image_tensor = transform(image=np.array(image))["image"]
    images.append(image_tensor)
    image_names.append(img_name)

# do the prediction with batch size 16 by padding all images to the biggest image size in the batch
# batch_size = 16
# for i in tqdm(range(0, len(images), batch_size)):
#     batch_images = images[i:i+batch_size]
#     batch_images = collate_fn(batch_images)
#     preds = lit_model.model.predict(batch_images.float())
#     for j in range(len(preds)):
#         decoded = lit_model.tokenizer.decode(preds[j].tolist())  # type: ignore
#         decoded_str = " ".join(decoded)
#         with open(os.path.join(output_path, image_names[i+j][:-4] + '.txt'), 'a', encoding='utf-8') as f:
#             f.write(decoded_str)

# rewrite the code above to do the infere in gpu
batch_size = 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
lit_model.model.to(device)
for i in tqdm(range(0, len(images), batch_size)):
    batch_images = images[i:i+batch_size]
    batch_images = collate_fn(batch_images)
    batch_images = batch_images.to(device)
    preds = lit_model.model.predict(batch_images.float())
    for j in range(len(preds)):
        decoded = lit_model.tokenizer.decode(preds[j].tolist())  # type: ignore
        decoded_str = " ".join(decoded)
        with open(os.path.join(output_path, image_names[i+j][:-4] + '.txt'), 'a', encoding='utf-8') as f:
            f.write(decoded_str)
