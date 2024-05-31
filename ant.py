class Ant():
    def __init__(self,  i, j):
        self.pathHistory = []
        self.position = self.moveTo(i, j) #Start position Ini
        self.pheromon = 1

    def getPheromon(self):
        return self.pheromon / len(self.pathHistory)

    def moveTo(self, n_i, n_j):
        self.position = (n_i, n_j)
        self.pathHistory.append(self.position)
        return self.position

    def resetMemory(self):
        self.pathHistory.clear()

    def getPosition(self):
        return self.position