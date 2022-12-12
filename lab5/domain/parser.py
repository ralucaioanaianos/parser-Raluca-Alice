from domain.grammar import Grammar


class Parser:
    def __init__(self, grammar: Grammar, w: str):
        self.i = 0
        self.alpha = []  # working stack
        self.beta = []  # input stack
        # self.alphaList = []
        self.grammar = grammar
        self.w = [w]
        self.state = "q"
        self.beta.append(self.grammar.getStartingSymbol())

    # def eliminateProductionsFromBeta(self, currentNonterminal, productionNumber):
    #     currentProductionInBeta = self.grammar.getProductionsFor(currentNonterminal)[1]
    #     j = 0

    def success(self):
        self.state = "f"
        self.beta.append("epsilon")

    def expand(self):
        currentNonTerminal = self.beta.pop()
        self.alpha.append(currentNonTerminal + " 0")
        productionsOfCurrentNonTerminal = self.grammar.getProductionsFor(currentNonTerminal)
        production = productionsOfCurrentNonTerminal[0]
        for j in range(len(production) - 1, 0, -1):
            self.beta.append(production[j])

    def advance(self):
        if self.beta[-1] != "epsilon":
            self.i += 1
        self.alpha.append(self.beta.pop())

    def momentaryInsuccess(self):
        self.state = "b"

    def back(self):
        self.state = "b"
        if self.alpha[-1] is not "epsilon":
            self.i -= 1
        self.beta.append(self.alpha.pop())

    def anotherTry(self):
        currentProduction = self.alpha.pop()
        currentNonterminal = currentProduction.split(" ")
        allProductions = self.grammar.getProductionsFor(currentNonterminal)
        pass

    def descendingRecursiveParsing(self):
        self.grammar.solveLeftRecursivity()

        while self.state != "f" and self.state != "e":
            if self.state == "q":
                if self.i == len(self.w) and len(self.beta) == 0:
                    self.success()
                elif len(self.beta) == 0:
                    self.back()
                # head of beta (input stack) is nonterminal
                elif self.beta[-1] in self.grammar.getNonterminals():
                    self.expand()
                # head of beta is a terminal = to current symbol from input
                elif self.i < len(self.w) and (self.beta[-1] == self.w[self.i] or self.beta[-1] == "epsilon"):
                    self.advance()
                else:
                    self.momentaryInsuccess()
            elif self.state == "b":
                if self.alpha[-1] in self.grammar.getTerminals():
                    self.back()
                else:
                    self.anotherTry()

        if self.state == "f":
            print("sequence accepted")
            # getAlphaAsList()
            # getProductionsString()
            # GetDerivationsString()
        else:
            print("error!")

