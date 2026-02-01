import os
import numpy as np
from PIL import Image

def convert_txt_to_image(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            header = f.readline().split()
            height, width = int(header[0]), int(header[1])

        print(f"Loading: {os.path.basename(input_file)} ({width}x{height})...")
        matrix = np.loadtxt(input_file, skiprows=1)

        if matrix.shape != (height, width):
            matrix = matrix.reshape((height, width))

        print(f"Min={matrix.min()}, Max={matrix.max()}")

        matrix = np.abs(matrix)
        matrix = np.clip(matrix, 0, 255)

        img_array = matrix.astype(np.uint8)

        img = Image.fromarray(img_array, mode='L')
        img.save(output_file)
        print(f"Pic successfully generated: {output_file}\n")

    except Exception as e:
        print(f"Error processing {input_file}: {e}\n")

INPUT_DIR = '../data/input_matrices'
OUTPUT_DIR = '../data/result_images'

if __name__ == "__main__":
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
    
    for file_name in files:
        input_path = os.path.join(INPUT_DIR, file_name)
        output_name = os.path.splitext(file_name)[0] + ".png"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        
        convert_txt_to_image(input_path, output_path)