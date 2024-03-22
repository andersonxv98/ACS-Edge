class Vizinho():
    def __init__(self, pi, pj):
        self.pi = pi
        self.pj = pj
        self.pheromon = 0
        self.intensidade = 0

    def getPheromon(self):
        return self.pheromon

    def setPheromon(self, pheromonNum):
        self.pheromon =pheromonNum

    def getIntensidade(self):
        return self.intensidade

    def setIntensidade(self, intensidadeNum):
        self.intensidade = intensidadeNum