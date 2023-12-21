import os
import shutil
import subprocess
import sys
from pathlib import Path
import image_to_latex.data.utils as utils

METADATA = {
    "im2latex_formulas.norm.lst": r"J:\github\image-to-latex\data\chungongshi\im2latex_formulas.norm.new.lst",
    "im2latex_validate_filter.lst": r"J:\github\image-to-latex\data\chungongshi\im2latex_validate_filter.lst",
    "im2latex_train_filter.lst": r"J:\github\image-to-latex\data\chungongshi\im2latex_train_filter.lst",
    "im2latex_test_filter.lst": r"J:\github\image-to-latex\data\chungongshi\im2latex_test_filter.lst",
    "formula_images": r"J:\github\image-to-latex\data\chungongshi\formula_images",
}
PROJECT_DIRNAME = Path(__file__).resolve().parents[1]
DATA_DIRNAME = PROJECT_DIRNAME / "data"
RAW_IMAGES_DIRNAME = METADATA["formula_images"]
PROCESSED_IMAGES_DIRNAME = Path(r'J:\github\image-to-latex\data\chungongshi\formula_images_processed')
VOCAB_FILE = PROJECT_DIRNAME / "image_to_latex" / "data" / "vocab.json"


def main():
    DATA_DIRNAME.mkdir(parents=True, exist_ok=True)
    cur_dir = os.getcwd()
    os.chdir(DATA_DIRNAME)

    # Skip downloading, use local files
    # for filename, local_path in METADATA.items():
    #     if local_path == r"I:\datasets\archive\formula_images_processed\formula_images_processed":
    #         continue
    #     local_path = Path(local_path)
    #     if not local_path.is_file():
    #         print(f"File not found: {local_path}")
    #         sys.exit(1)
    #     else:
    #         # Copy the local file to the destination directory
    #         destination_path = DATA_DIRNAME / filename
    #         if not destination_path.is_file():
    #             shutil.copy(local_path, destination_path)

    # Extract regions of interest
    if not PROCESSED_IMAGES_DIRNAME.exists():
        PROCESSED_IMAGES_DIRNAME.mkdir(parents=True, exist_ok=True)
        print("Cropping images...")
        count = 0
        for image_filename in Path(RAW_IMAGES_DIRNAME).glob("*.png"):
            count += 1
            cropped_image = utils.crop(image_filename, padding=8)
            if not cropped_image:
                continue
            cropped_image.save(PROCESSED_IMAGES_DIRNAME / image_filename.name)
            if count % 1000 == 0:
                print(f"{count} images cropped")

    os.chdir(cur_dir)


if __name__ == "__main__":
    main()



