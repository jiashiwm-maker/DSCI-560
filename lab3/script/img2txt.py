import os
import numpy as np
from PIL import Image

def convert_images_to_txt(input_folder, output_folder, file_list):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in file_list:
        file_path = os.path.join(input_folder, file_name)
        
        try:
            img = Image.open(file_path)
            img_gray = img.convert('L')
            img_array = np.array(img_gray, dtype=int)
            height, width = img_array.shape
            
            print(f"Processing: {file_name} | Size: {width}x{height}")
            if width not in [512, 1024, 2048]:
                print(f"Size not correct!")

            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(output_folder, base_name + ".txt")

            np.savetxt(output_path, img_array, fmt='%d', header=f"{height} {width}", comments='')
            
            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

INPUT_DIR = '../data/input_images'
OUTPUT_DIR = '../data/output_matrices'

MY_IMAGES = [
    'test_1.png',
    'test_2.png',
    'test_3.png'
]

if __name__ == "__main__":
    convert_images_to_txt(INPUT_DIR, OUTPUT_DIR, MY_IMAGES)