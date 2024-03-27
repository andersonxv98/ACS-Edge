import decimal

from PIL import Image, ImageOps
import numpy as np
from ant import Ant
from vizinho import Vizinho

class ACSEdgeImage():
    def __init__(self, path, initial_pheromone, coef_queda, coef_evap_q):
        self.path = path
        self.im = self.loadImg()
        #self.resize(50,50) #redimensionar a imagem para testes rapidos
        self.mtx_perom = np.full(self.im.size,float(initial_pheromone),dtype=float) #representação dos feromonios na imagem
        print("(CONTRUCTOR) MATRIX FEROMN: ", self.mtx_perom)
        self.mtx_heuristc = np.full(self.im.size,0,dtype=np.uint8)
        self.ants = []
        self.q0 = None
        self.Tinit = None
        self.coeficiente_de_queda = coef_queda #
        self.coef_evaporac_p =coef_evap_q
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

        if(result == 0):
            print("HEURISTIC INFORMATION: ", result, " POSITION: ", (i,j), " V1: ", v1)
        return float(result)

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

        return float(ph)

    def getPseudoRandomProportional(self, i , j, lastPositionVisited):

        print("PASSO 2.1 (PSEUDO RANDOM PROPORTIONAL")
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
                if(heuristicInfo == 0):
                    print("SVIZINHANÇA: ", somaVizinhanca, " PHEROMON: ",phFromPx , " HEURISCTI: ", heuristicInfo)
                    pseudorandom2 = 1

                pseudorandom = pseudorandom1/pseudorandom2

                if(pseudorandom >= maxValue):
                    if(lastPositionVisited[0] != neighbor.pi and lastPositionVisited[1] != neighbor.pj ):
                        maxValue = pseudorandom
                        Nextposition = (neighbor.pi, neighbor.pj)



        print("NEXT POSITION: ", Nextposition)
        return Nextposition, maxValue


    def setPeromValueFromPixel(self, i, j, val):
        print("Atualizou, Anterior: ", self.mtx_perom[i,j], " Atual: ", val)
        self.mtx_perom[i,j] = val
        return
    def updateLocalPheromone(self, i ,j, iteration):
        print("PASSO 2.2 ATUALIZAR FEROMONIO LOCAL")
        ferom = self.getPeromValueFromPixel(i,  j)

        coef_queda = float(self.coeficiente_de_queda)
        fero_inicial = float(self.Tinit) #valor do feromonio inicialmente
        local_feromon1 = ((1 - coef_queda) * ferom)
        local_feromon2 = (coef_queda * fero_inicial)
        local_feromon = float(local_feromon1 + local_feromon2)
        self.setPeromValueFromPixel(i, j, local_feromon)
        """
        print("feromonio: ", ferom)
        print("Coef_queda: ", coef_queda)
        print("local1: ", local_feromon1)
        print("local2: ", local_feromon2)
        print("LOCAL PHEROI : ", local_feromon)
        """



    def updateGlobalPheromone(self):
        print("PASSO 2.3 UPDATE GLOBAL: ")
        for i in range(len(self.mtx_perom)):
            for j in range(len(self.mtx_perom[0])):
                n_info_heuristic = 0
                soma_info_heuristic = 0
                ferom = self.getPeromValueFromPixel(i, j)
                for ant in self.ants:
                    if (i, j) in ant.pathHistory:
                        n_info_heuristic += 1
                        soma_info_heuristic += self.getHeuristicInformation(i, j)

                # isso deve ser igual a média das informações heuristicas associadas com o  pixelpertencente ao tuor dessa formiga
                qtd_ferom_depositado_no_pixel = (soma_info_heuristic/n_info_heuristic) if n_info_heuristic> 0 else 0
                new_feromon_value = ((1 - self.coef_evaporac_p) * ferom) + (
                            self.coef_evaporac_p * qtd_ferom_depositado_no_pixel)
                self.setPeromValueFromPixel(i, j, new_feromon_value)
        return


    def initACS(self, qtdAnts, initialPeromVal, iteration,qtdPconstrSteps, q0):
        print("PASSO 1: INICIALIZAR")
        self.Tinit = initialPeromVal
        self.q0 = q0
        self.createAnts(qtdAnts)
        for x in range(self.im.size[0]):
            for y in range(self.im.size[1]):
                h_info = self.getHeuristicInformation(x, y)
                self.mtx_heuristc[x, y] = h_info

        print("PASSO 1.1 : MTX: HEURISTIC INFORMATION: ", self.mtx_heuristc)
        print("PASSO 1.2 MTX: FEROM INICIAL: ", self.mtx_perom)
        self.runACS(iteration, qtdPconstrSteps, q0, qtdAnts)
        return

    def createAnts(self, qtd):
        for i in range(qtd):
            iip = np.random.randint(0, (self.im.size[0]))
            j = np.random.randint(0, (self.im.size[1]))
            ant = Ant(iip, j)
            #self.updateLocalPheromone(ant.position[0], ant.position[1], 0)
            self.ants.append(ant)



    def runACS(self, iteration,qtdPcontr, q0, qtdAnts):
        print("PASSO 2: Contrução iterativa e Processo de Atualização")
        for n in range(iteration): #iteração por quantidade de iteração
            for c in range(qtdPcontr): #passos por quantidade de passos
                for ant in self.ants: #para cada formiga no formigueiro
                    i0, j0 = ant.position #posição atual da formiga (pixel que se encontra na imagem)
                    # probabilidade de transição por biased exploration
                        #busca o pixel com maior probabilidade de transição a partir da posição do pixel atual
                    recente_visitado = ant.pathHistory[len(ant.pathHistory)-2] if c > 0 else ant.position

                    psdS, psdRandPropVAl = self.getPseudoRandomProportional(i0, j0, recente_visitado)
                    psdRandX = psdS[0]
                    psdRandY = psdS[1]
                    ant.moveTo(psdRandX, psdRandY)
                    #atualiza  pherom local
                    self.updateLocalPheromone(psdRandX,psdRandY, n)


            #print(self.mtx_perom)
            #return
            self.updateGlobalPheromone()

        print(self.mtx_perom)