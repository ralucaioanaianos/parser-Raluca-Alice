class Grammar:

    def __init__(self):
        self.N = []  # nonterminals
        self.E = []  # terminals
        self.S = ""  # start symbol
        self.P = {}  # predictions

    def readFromFile(self, file):
        with open(file, "r") as f:
            self.N = f.readline().strip().split(" : ")[1].split(" ")
            self.E = f.readline().strip().split(" : ")[1].split(" ")
            self.S = f.readline().strip().split(" : ")[1]

            f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                left, right = line.strip().split(" -> ")
                right = [value.strip().split() for value in right.split(' | ')]
                self.P[left] = right

    def getNonterminals(self):
        return self.N

    def getTerminals(self):
        return self.E

    def getProductions(self):
        return self.P

    def getProductionsFor(self, nonterminal: str):
        if nonterminal in self.P.keys():
            return self.P[nonterminal]
        return None

    def elementInGrammar(self, element):
        if not (element in self.N or element == "epsilon" or element in self.E):
            return False
        return True

    def CFGCheck(self):
        if self.S not in self.N:
            return False
        for key in self.P.keys():
            if key not in self.N:
                return False
            for production in self.P[key]:
                for element in production:
                    if not self.elementInGrammar(element):
                        return False
        return True



