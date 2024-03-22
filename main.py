from image import ACSEdgeImage
from ant import Ant
import numpy as np
def main():
    #print("Hello World!")
    im = ACSEdgeImage("ImageTests/lena.png")
    im.showImg()
    im.initACS(512,0.1, 2, 40, 0.5)
    #im.showImg()
    #intensidade = im.getPixelIntensityValue(100,100)
    #print("INtensidade: ", intensidade)


main()