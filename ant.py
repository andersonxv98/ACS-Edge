
class Ant():
    def __init__(self,  i, j):
        self.pathHistory = []
        self.position = self.moveTo(i, j) #Start position Ini


    def moveTo(self, n_i, n_j):
        self.position = (n_i, n_j)

        self.pathHistory.append(self.position)
        return self.position


    def getPosition(self):
        return self.position


