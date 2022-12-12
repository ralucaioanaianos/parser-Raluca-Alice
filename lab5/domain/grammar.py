class Grammar:

    def __init__(self):
        self.N = []  # nonterminals
        self.T = []  # terminals
        self.S = ""  # start symbol
        self.P = {}  # productions

    def readFromFile(self, file):
        with open(file, "r") as f:
            self.N = f.readline().strip().split(" : ")[1].split(" ")
            self.T = f.readline().strip().split(" : ")[1].split(" ")
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
        return self.T

    def getProductions(self):
        return self.P

    def getProductionsFor(self, nonterminal: str):
        if nonterminal in self.P.keys():
            return self.P[nonterminal]
        return None

    def elementInGrammar(self, element):
        if not (element in self.N or element == "epsilon" or element in self.T):
            return False
        return True

    def getStartingSymbol(self):
        return self.S

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

    def solveLeftRecursivity(self):
        auxProductions = {}

        for lhs in self.P.keys():
            # print(lhs)
            leftRecursiveProductions = list(filter(lambda p: p[0] == lhs, self.P[lhs]))
            if len(leftRecursiveProductions) > 0:
                newProductionsForLHS = []
                auxNonTerminal = lhs + "Aux"
                newProductionsForAux = []

                hasBeta = False

                for rhs in self.P[lhs]:
                    if rhs not in leftRecursiveProductions:
                        newProductionsForLHS.append(rhs)
                        newProductionsForLHS[-1].append(auxNonTerminal)
                        hasBeta = True
                    else:
                        newProd = []
                        for i in range(1, len(rhs)):
                            newProd.append(rhs[i])
                        newProd.append(auxNonTerminal)
                        newProductionsForAux.append(newProd)

                newProductionsForAux.append(["epsilon"])

                if not hasBeta:
                    raise Exception("Left recursive production without beta!")

                auxProductions[auxNonTerminal] = newProductionsForAux
                self.N.append(auxNonTerminal)
                if "epsilon" not in self.T:
                    self.T.append("epsilon")
                self.P[lhs] = newProductionsForLHS

        for lhs in auxProductions.keys():
            self.P[lhs] = auxProductions[lhs]


