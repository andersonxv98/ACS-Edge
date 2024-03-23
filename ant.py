class Ant():
    def __init__(self,  i, j):
        self.pathHistory = []
        self.position = (i, j) #Start position Ini


    def moveTo(self, n_i, n_j):
        if (n_i, n_j) not in self.pathHistory:
            self.position = (n_i, n_j)
            self.pathHistory.append(self.position)
            return


    def getPosition(self):
        return self.position


