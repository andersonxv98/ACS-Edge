class Neighbor():
    def __init__(self, pi, pj):
        self.pi = pi
        self.pj = pj
        self.pheromon = 0
        self.intensity = 0

    def getPheromon(self):
        return self.pheromon

    def setPheromon(self, pheromonNum):
        self.pheromon = pheromonNum

    def getIntensity(self):
        return self.intensity

    def setIntensity(self, intensityNum):
        self.intensity = intensityNum