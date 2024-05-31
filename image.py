from PIL import Image
import numpy as np
from ant import Ant
from neighbor import Neighbor
class ACSEdgeImage():
    def __init__(self, path, initial_pheromone, coef_queda, coef_evap_q, p):
        self.path = path
        self.img = self.loadImg()
        self.resize(256,256) #redimensionar a imagem para testes rapidos
        self.mtx_pherom = np.full(self.img.size,float(initial_pheromone),dtype=float) #representação dos feromonios na imagem
        self.ants = []
        self.q0 = None
        self.p = p
        self.Tinit = None
        self.coeficiente_de_queda = coef_queda
        self.coef_evaporac_p = coef_evap_q

    def loadImg(self):
        return Image.open(self.path).convert('L')  # grayscale

    def resize(self, width, height):
        self.img = self.img.resize((width, height))

    def showImg(self):
        self.img.show()

    def getPixelIntensityValue(self, i, j):
        return self.img.getpixel((i, j))

    def getNeighbors8(self, i, j):
        neighbors = []
        for ni, nj in [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]:
            neighbor = Neighbor(ni, nj)
            neighbors.append(neighbor)
            neighbor.setIntensity(self.tratamentoGetPixel(ni, nj))
        return neighbors

    def tratamentoGetPixel(self, i, j):
        try:
            return self.getPixelIntensityValue(i, j)
        except:
            return 0

    def getLocalGroupOfPixels(self, i, j):
        neighbors = self.getNeighbors8(i, j)
        vcl_geral = sum(abs(neighbors[k].intensity - neighbors[k + 4].intensity) for k in range(4))
        return vcl_geral

    def getVmax(self):
        return np.max(np.asarray(self.img))

    def getHeuristicInformation(self, i, j):
        v1 = self.getLocalGroupOfPixels(i, j)
        v2 = self.getVmax()  # busca a intensidade máxima de variação de toda a imagem
        return v1 / v2 if v2 != 0 else 0.0

    def sumValuesFromNeighborhood(self, i, j):
        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i,j)
        return (
            topLeft.getIntensity()
            + topCenter.getIntensity()
            + topRight.getIntensity()
            + centerLeft.getIntensity()
            + centerRight.getIntensity()
            + bottomLeft.getIntensity()
            + bottomCenter.getIntensity()
            + bottomRight.getIntensity()
        )

    def getPheromValueFromPixel(self, i, j):
        try:
            return float(self.mtx_pherom[i, j])
        except:
            return 0.0

    def getPseudoRandomProportional(self, i , j, lastPositionVisited):
        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i, j)
        somaVizinhanca  = self.sumValuesFromNeighborhood(i, j)
        neigt8 = [topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight]
        maxValue = 0
        Nextposition = (i, j)

        for neighbor in neigt8:
            npi= neighbor.pi
            npj = neighbor.pj

            if (npi >= 0 and npi < self.img.size[0]):
                if npj >= 0 and npj < self.img.size[1]:
                    phFromPx = self.getPheromValueFromPixel(npi, npj)
                    heuristicInfo = self.getHeuristicInformation(npi, npj)

                    pseudorandom1 = (phFromPx * heuristicInfo)
                    pseudorandom2 = (somaVizinhanca *(phFromPx * heuristicInfo))
                    if(heuristicInfo == 0 or phFromPx == 0):
                        pseudorandom2 = 1

                    pseudorandom = pseudorandom1/pseudorandom2

                    if(pseudorandom >= maxValue):
                        if(lastPositionVisited[0] != neighbor.pi and lastPositionVisited[1] != neighbor.pj ):
                            maxValue = pseudorandom
                            Nextposition = (neighbor.pi, neighbor.pj)

        return Nextposition, maxValue

    def setPeromValueFromPixel(self, i, j, val):
        self.mtx_pherom[i][j] = val

    def updateLocalPheromone(self, i ,j, ferom):
        self.setPeromValueFromPixel(i, j, (1 - float(self.coeficiente_de_queda)) * ferom + float(self.Tinit) * float(self.coeficiente_de_queda))

    def updateGlobalPheromone(self):
        for i in range(len(self.mtx_pherom)):
            for j in range(len(self.mtx_pherom[i])):
                n_info_heuristic = 0
                soma_info_heuristic = 0
                ferom = self.getPheromValueFromPixel(i, j)

                for ant in self.ants:
                    if (i, j) in ant.pathHistory:
                        n_info_heuristic += 1
                        soma_info_heuristic += self.getHeuristicInformation(i, j)

                # deve ser igual a média das informações heuristicas associadas com o  pixel pertencente ao tutor dessa formiga
                qtd_ferom_depositado_no_pixel = (soma_info_heuristic/n_info_heuristic) if n_info_heuristic> 0 else 0
                new_feromon_value = ((1 - self.coef_evaporac_p) * ferom) + (
                            self.coef_evaporac_p * qtd_ferom_depositado_no_pixel)
                self.setPeromValueFromPixel(i, j, new_feromon_value)

    def initACS(self, qtdAnts, initialPeromVal, iteration,qtdPconstrSteps, q0):
        self.Tinit = initialPeromVal
        self.q0 = q0
        self.createAnts(qtdAnts)
        self.runACS(iteration, qtdPconstrSteps, q0)
        return self.mtx_pherom

    def getSumPheromNeigtborhood(self, i, j):
        return sum(self.getPheromValueFromPixel(x, y) for x in range(i-1, i+2) for y in range(j-1, j+2) if 0 <= x < self.img.size[0] and 0 <= y < self.img.size[1])


    def getSumHeuristic(self, i , j):
        return sum(self.getHeuristicInformation(x, y) for x in range(i-1, i+2) for y in range(j-1, j+2) if 0 <= x < self.img.size[0] and 0 <= y < self.img.size[1])


    def getPointTransitionProb(self, i, j, lastp):
        topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight = self.getNeighbors8(i, j)

        neigt8 = [topLeft, topCenter, topRight, centerLeft, centerRight, bottomLeft, bottomCenter, bottomRight]
        pro_val = 0
        Nextposition = (i, j)
        for neighbor in neigt8:
            npi= neighbor.pi
            npj = neighbor.pj
            if npi != lastp[0] and npj != lastp[1]:
                if(npi >= 0 and npj >= 0 and npi < self.img.size[0] and npj < self.img.size[1]):
                    prob = self.transitionPropability((i, j), (npi, npj))

                    if prob >= pro_val:
                        pro_val = prob
                        Nextposition = (npi, npj)

        return Nextposition

    def transitionPropability(self, Pi , Pj):
        Tij = self.getPheromValueFromPixel(*Pi) + self.getPheromValueFromPixel(*Pj)
        Nij = self.getHeuristicInformation(*Pi) + self.getHeuristicInformation(*Pj)
        part1 = Tij * Nij
        part2 = self.getSumPheromNeigtborhood(*Pi) * self.getSumHeuristic(*Pi)
        return part1 / part2 if part2 != 0 else 0

    def createAnts(self, qtd):
        self.ants = [Ant(np.random.randint(0, self.img.size[0]), np.random.randint(0, self.img.size[1])) for _ in range(qtd)]

    def runACS(self, iteration, qtd_p_contr, q0):
        for n in range(iteration):
            for c in range(qtd_p_contr):
                for ant in self.ants:
                    i0, j0 = ant.position
                    recente_visitado = ant.pathHistory[-2] if c > 0 else ant.position

                    if self.p <= q0:
                        psd_s, psd_rand_prop_val = self.getPseudoRandomProportional(i0, j0, recente_visitado)
                    else:
                        psd_s = self.getPointTransitionProb(i0, j0, recente_visitado)

                    psd_rand_x, psd_rand_y = psd_s
                    ant.moveTo(psd_rand_x, psd_rand_y)
                    feromonio = ant.getPheromon()

                    self.updateLocalPheromone(psd_rand_x, psd_rand_y, feromonio)

            self.updateGlobalPheromone()