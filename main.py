from image import ACSEdgeImage
from ant import Ant
import numpy as np
def main():
    #print("Hello World!")
    initial_pherom = 0.1 #deve ser valor maior que zero (0,1]
    im = ACSEdgeImage("ImageTests/lena.png", initial_pherom, 0.05)
    im.showImg()
    im.initACS(100,initial_pherom, 10, 40, 0.5)
    #im.showImg()
    #intensidade = im.getPixelIntensityValue(100,100)
    #print("INtensidade: ", intensidade)


main()