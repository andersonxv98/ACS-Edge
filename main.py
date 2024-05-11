from image import ACSEdgeImage
from ant import Ant
from skimage import filters
from PIL import Image
import numpy as np
import random
def main():
    #print("Hello World!")
    initial_pherom = 0.1 #deve ser valor maior que zero (0,1]
    p = random.uniform(0, 1) #VALOR DE P GERADO UNIFORMEMENTE ENTRE 0 e 1 (CONDIÇÇÂO ACS)
    print("VALO P: ", p)
    for i in range(1,10):
        im = ACSEdgeImage("ImageTests/lena.png", initial_pherom, 0.05, 0.1, p=p)
        im.showImg()
        q0 = i / 10
        img_phero = im.initACS(1024,initial_pherom, 10, 40, q0)
        #Image.fromarray(np.array(img_phero)).show()
        print("IMG PHERO: ", img_phero)
        img_phero_ = img_phero
        limiar_otsu = filters.threshold_otsu(img_phero_)
        print("Shape of img_phero:", img_phero.shape)  # Add this line to check the shape
        print("Value of limiar_otsu:", limiar_otsu) 
        img_bin = img_phero > limiar_otsu
    
        im = Image.fromarray((img_bin.T * 255).astype(np.uint8))
        im.save("./"+"lana_LastTest"+str(i)+".png")
        #intensidade = im.getPixelIntensityValue(100,100)
        #print("INtensidade: ", intensidade)

        #return
main()