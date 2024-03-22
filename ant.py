class Ant():
    def __init__(self,  i, j):
        self.pathHistory = []
        self.position = self.moveTo(i,j) #Start position Ini


    def moveTo(self, n_i, n_j):
        if (n_i, n_j) not in self.pathHistory:
            position = (n_i, n_j)
            self.pathHistory.append(position)
            return position


    def getPosition(self):
        return self.position


