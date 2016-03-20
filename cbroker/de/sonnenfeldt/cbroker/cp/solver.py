from Numberjack import Variable

class CBrokerSolver():
    
    model = None
    
    def __init__(self, model):
        self.model = model

    def solve(self):
        self.s = self.model.m.load('Mistral')
        self.s.setVerbosity(1)
    
        res = self.s.solve()
        self.s.printStatistics()
        return res
    
    def getNextSolution(self):
        return self.s.getNextSolution()