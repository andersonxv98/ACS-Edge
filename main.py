from image import ACSEdgeImage
from PIL import Image
import numpy as np
from skimage import filters
import random
from tqdm import tqdm
from datetime import datetime
import os

def main():
    initial_pherom = 0.1
    p = random.uniform(0, 1)
    iterations = 10
    ants_count = 100 #lena (256x256) => 500
    steps_per_construction = 40
    q0 = 0.5

    # Cria uma pasta para guardar os resultados
    timestamp = datetime.now().strftime("%Y-%m-%dT%Hh%Mmin%Sseg")
    output_folder = f"Output/{timestamp}"
    os.makedirs(output_folder, exist_ok=True)

    for i in tqdm(range(iterations), desc="Progresso do Algoritmo ACS"):
        img = ACSEdgeImage("Input/pikachu.png", initial_pherom, 0.05, 0.1, p=p)
        q0 = i / 10
        img_phero = img.initACS(ants_count, initial_pherom, iterations, steps_per_construction, q0)

        # Aplicando o limiar Otsu
        threshold_otsu = filters.threshold_otsu(img_phero)
        img_bin = img_phero > threshold_otsu

        # Convertendo a imagem binária para uint8 e salvando o resultado
        img_bin = Image.fromarray((img_bin.T * 255).astype(np.uint8))
        imag_name = f"pikachu_resultado_q0={q0}.png"
        img_bin.save(os.path.join(output_folder, imag_name))

if __name__ == "__main__":
    main()