import decimal

from PIL import Image, ImageOps
import numpy as np
from ant import Ant
from vizinho import Vizinho
class ACSEdgeImage():
    def __init__(self, path, initial_pheromone, coef_queda):
        self.path = path
        self.im = self.loadImg()
        self.resize(50,50)
        self.mtx_perom = np.full(self.im.size,float(initial_pheromone),dtype=decimal.Decimal) #representação dos feromonios na imagem
        print("(CONTRUCTOR) MATRIX FEROMN: ", self.mtx_perom)
        self.mtx_heuristc = np.full(self.im.size,0,dtype=np.uint8)
        self.ants = []
        self.q0 = None
        self.Tinit = None
        self.coeficiente_de_queda = coef_queda #
    def loadImg(self):
        im = Image.open(r""+self.path)
        im = ImageOps.grayscale(im)


        return im

    def resize(self, width, height):
        self.im = self.im.resize((width, height))
        return
    def showImg(self):
        self.im.show()
        print(self.im.size)
    def getPixelIntensityValue(self, i, j):
        result = self.im.getpixel((i, j))
        return result

    def getNeighbors8(self, i, j):

        TopLeft = Vizinho(i - 1, j - 1)
        TopCenter = Vizinho(i - 1, j)
        TopRight = Vizinho(i - 1, j + 1)
        CenterLeft = Vizinho(i, j - 1)
        CenterRight = Vizinho(i, j + 1)
        BottomLeft = Vizinho(i + 1, j - 1)
        BottomCenter = Vizinho(i + 1, j)
        BottomRight = Vizinho(i + 1, j + 1)


        topLeftVal = self.tratamentoGetPixel(i - 1, j - 1)
        topCenterVal = self.tratamentoGetPixel(i - 1, j)
        topRightVal = self.tratamentoGetPixel(i - 1, j + 1)
        centerLeftVal = self.tratamentoGetPixel(i, j - 1)
        centerRightVal = self.tratamentoGetPixel(i, j + 1)
        bottomLeftVal = self.tratamentoGetPixel(i + 1, j - 1)
        bottomCenterVal = self.tratamentoGetPixel(i + 1, j)
        bottomRightVal = self.tratamentoGetPixel(i + 1, j + 1)


        TopLeft.setIntensidade(topLeftVal)
        TopCenter.setIntensidade(topCenterVal)
        TopRight.setIntensidade(topRightVal)
        CenterLeft.setIntensidade(centerLeftVal)
        CenterRight.setIntensidade(centerRightVal)
        BottomLeft.setIntensidade(bottomLeftVal)
        BottomCenter.setIntensidade(bottomCenterVal)
        BottomRight.setIntensidade(bottomRightVal)

        return TopLeft, TopCenter, TopRight, CenterLeft, CenterRight, BottomLeft, BottomCenter, BottomRight

    def tratamentoGetPixel(self, i ,j):

        try:
            res = self.getPixelIntensityValue(i, j)
        except:
            res = 0

        return res

    def getLocalGroupOfPixels(self, i, j):

        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i,j)
        VcLij1 =  (topLeft.getIntensidade() - bottomRight.getIntensidade()) if (topLeft.getIntensidade() - bottomRight.getIntensidade()) >= 0 else ((topLeft.getIntensidade() - bottomRight.getIntensidade()) * -1)
        VcLij2 = (topCenter.getIntensidade() - bottomCenter.getIntensidade()) if (topCenter.getIntensidade() - bottomCenter.getIntensidade()) >= 0 else ((topCenter.getIntensidade() - bottomCenter.getIntensidade()) * -1)
        VcLij3 = (topRight.getIntensidade() - bottomLeft.getIntensidade()) if (topRight.getIntensidade() - bottomLeft.getIntensidade()) >= 0 else ((topRight.getIntensidade() - bottomLeft.getIntensidade())* -1)
        VcLij4 = (centerLeft.getIntensidade() - centerRight.getIntensidade()) if (centerLeft.getIntensidade() - centerRight.getIntensidade()) >= 0 else ((centerLeft.getIntensidade() - centerRight.getIntensidade())* -1)

        VCLGeral = VcLij1 + VcLij2 + VcLij3 + VcLij4

        return VCLGeral

    def getVmax(self):
        m = np.asarray(self.im).max()
        #print("Intensidade Maxima: ", m)
        return m

    def getHeuristicInformation(self, i, j):
        v1 = self.getLocalGroupOfPixels(i, j)
        v2 = self.getVmax() #busca a intensidade maxima de variação de toda a imagem
        result = v1/v2
        return decimal.Decimal(result)

    def sumValuesFromNeighborhood(self, i, j):
        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i,j)
        somaDosValoresDaVizinhaca= (topLeft.getIntensidade() + topCenter.getIntensidade() + topRight.getIntensidade()
                                    + centerLeft.getIntensidade() + centerRight.getIntensidade() + bottomLeft.getIntensidade()
                                    + bottomCenter.getIntensidade()+bottomRight.getIntensidade())
        return somaDosValoresDaVizinhaca

    def getPeromValueFromPixel(self, i, j):
        ph = 0
        try:
            ph = self.mtx_perom[i, j]
        except:
            print("Error:")

        return decimal.Decimal(ph)

    def getPseudoRandomProportional(self, i , j):


        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i, j)
        somaVizinhanca  = self.sumValuesFromNeighborhood(i, j)
        neigt8 = [topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight]
        maxValue = 0
        Nextposition = (i, j)
        for neighbor in neigt8:

            npi= neighbor.pi
            npj = neighbor.pj
            if (npi >= 0 and npj >= 0 and npi < self.im.size[0] and npj < self.im.size[1]):

                phFromPx = self.getPeromValueFromPixel(npi, npj)
                heuristicInfo = self.getHeuristicInformation(npi, npj)

                pseudorandom1 = (phFromPx * heuristicInfo)
                pseudorandom2 = (somaVizinhanca *(phFromPx * heuristicInfo))
                pseudorandom = pseudorandom1/pseudorandom2

                if(pseudorandom >= maxValue):
                    maxValue = pseudorandom
                    Nextposition = (neighbor.pi, neighbor.pj)




        return Nextposition


    def setPeromValueFromPixel(self, i, j, val):
        if(self.mtx_perom[i, j] != val):
            #print("Atualizou, Anterior: ", self.mtx_perom[i,j], " Atual: ", val)
            self.mtx_perom[i,j] = val
        return
    def updateLocalPheromone(self, i ,j):
        ferom = self.getPeromValueFromPixel(i,  j)

        coef_queda = decimal.Decimal(self.coeficiente_de_queda)
        fero_inicial = decimal.Decimal(self.Tinit) #valor do feromonio inicialmente
        local_feromon1 = ((1 - coef_queda) * ferom)
        local_feromon2 = (coef_queda * fero_inicial)
        local_feromon = decimal.Decimal(local_feromon1 + local_feromon2)

        #print("feromonio: ", ferom)
        #print("Coef_queda: ", coef_queda)
        #print("local1: ", local_feromon1)
        #print("local2: ", local_feromon2)
        #print("LOCAL PHEROI : ", local_feromon)
        self.setPeromValueFromPixel(i, j, local_feromon)
        return


    def updateGlobalPheromone(self):
        return
        ferom = self.getPeromValueFromPixel(i,j)
        qtd_ferom_depositado_no_pixel = 0 #isso deve ser igual a média das informações heuristicas associadas com o  pixelpertencente ao tuor dessa formiga
        coef_evaporac_p = 0 #zero a 1
        global_feromon = ((1 - coef_evaporac_p) * ferom ) + (coef_evaporac_p * qtd_ferom_depositado_no_pixel)

        return global_feromon


    def initACS(self, qtdAnts, initialPeromVal, iteration,qtdPconstrSteps, q0):
        self.Tinit = initialPeromVal
        self.q0 = q0
        for i in range(qtdAnts):
            iip = np.random.randint(0, (self.im.size[0]))
            j = np.random.randint(0, (self.im.size[1]))
            ant = Ant(iip, j)
            self.ants.append(ant)
        for x in range(self.im.size[0]):
            for y in range(self.im.size[1]):
                h_info = self.getHeuristicInformation(x, y)
                self.mtx_heuristc[x, y] = h_info
        #print("MTX: HEURISTIC INFORMATION: ", self.mtx_heuristc)
        self.runACS(iteration, qtdPconstrSteps, q0)
        return

    def runACS(self, iteration,qtdPcontr, q0):
        for n in range(iteration): #iteração por quantidade de iteração
            for c in range(qtdPcontr): #passos por quantidade de passos
                for ant in self.ants: #para cada formiga no formigueiro
                    i0, j0 = ant.position #posição atual da formiga (pixel que se encontra na imagem)

                    # probabilidade de transição por biased exploration
                        #busca o pixel com maior probabilidade de transição a partir da posição do pixel atual
                    psdRandX, psdRandY = self.getPseudoRandomProportional(i0, j0)
                    ant.moveTo(psdRandX, psdRandY)
                    #atualiza  pherom local
                    self.updateLocalPheromone(psdRandX,psdRandY)
            print(self.mtx_perom)
            return
            self.updateGlobalPheromone()

        print(self.mtx_perom)