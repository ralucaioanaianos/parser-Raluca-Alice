from domain.grammar import Grammar
from domain.table_parser_output import TableOutput

NORMAL_STATE = "q"
BACK_STATE = "b"
FINAL_STATE = "f"
ERROR_STATE = "e"

EPSILON = "epsilon"


class Parser:
    def __init__(self, grammar: Grammar, w: str):
        self.state = NORMAL_STATE  # state of the parsing
        self.i = 0  # position of current symbol in input sequence
        self.alpha = []  # working stack, stores the way the parse is built
        self.beta = [grammar.getStartingSymbol()]  # input stack, part of the tree to be built
        self.grammar = grammar
        self.w = w.split(' ')  # the word/sequence
        self.f = open("demofile2.txt", "w")


    # ------------------------- MOVES -------------------------
    def expand(self):
        """
        WHEN: head of input stack is a nonterminal
            (q, i, ἄ, Aβ) ⊢ (q, i, ἄA1, γ1β)
        where:
        A → γ1 | γ2 | … represents the productions corresponding to A
        1 = first prod of A
        """
        self.f.write("-> expand\n")
        current_non_terminal = self.beta.pop()
        self.alpha.append(current_non_terminal + " 0")
        productions_of_current_non_terminal = self.grammar.getProductionsFor(current_non_terminal)
        production = productions_of_current_non_terminal[0]  # expand always gets first production
        for j in range(len(production) - 1, -1, -1):  # put it in stack in reverse order
            self.beta.append(production[j])

    def advance(self):
        """
        WHEN: head of input stack is a terminal = current symbol from input
            (q, i, ἄ, aiβ) ⊢ (q, i+1, ἄai, β)
        """
        self.f.write("-> advance\n")
        #print("-> advance", end="\n")
        if self.beta[-1] != EPSILON:
            self.i += 1
        self.alpha.append(self.beta.pop())

    def momentary_insuccess(self):
        """
        WHEN: head of input stack is a terminal ≠ current symbol from input
            (q, i, ἄ, aiβ) ⊢ (b, i, ἄ, aiβ)
        """
        self.f.write("-> momentary insuccess\n")
        #print("-> momentary insuccess", end="\n")
        self.state = BACK_STATE

    def back(self):
        """
        WHEN: head of working stack is a terminal
            (b, i, ἄa, β) ⊢ (b, i-1, ἄ, aβ)
        """
        self.f.write("-> back\n")
        #print("-> back", end="\n")
        self.state = BACK_STATE
        if self.alpha[-1] != EPSILON:
            self.i -= 1
        self.beta.append(self.alpha.pop())

    def another_try(self):
        """
        WHEN: head of working stack is a nonterminal
        (b, i, ἄ Aj, γj β) ⊢ (q, i, ἄ Aj+1, γj+1 β) , if ∃ A → γj+1
                             (b, i, ἄ, A β), otherwise with the exception
                             (e, i, ἄ, β), if i=1, A=S, ERROR
        """
        self.f.write("-> another try\n")
        #print("-> another try", end="\n")
        current_production = self.alpha.pop()
        non_terminal_and_production_number = current_production.split(" ")
        current_non_terminal = non_terminal_and_production_number[0]
        production_number = int(non_terminal_and_production_number[1])

        all_productions = self.grammar.getProductionsFor(current_non_terminal)

        self.eliminate_productions_from_beta(current_non_terminal, production_number)

        if production_number < len(all_productions)-1:
            new_production_number = production_number + 1
            self.alpha.append(current_non_terminal + " " + str(new_production_number))

            production = all_productions[new_production_number]
            for j in range(len(production)-1, -1, -1):
                self.beta.append(production[j])

            self.state = NORMAL_STATE
        else:
            if self.i == 0 and current_non_terminal == self.grammar.getStartingSymbol():
                self.state = ERROR_STATE
            else:
                self.beta.append(current_non_terminal)

    def success(self):
        """
        (q, n+1, ἄ, Ɛ) ⊢ (f, n+1, ἄ, Ɛ)
        :return:
        """
        self.f.write("-> success\n")
        #print("-> success", end="\n")
        self.state = FINAL_STATE
        self.beta.append(EPSILON)

    def eliminate_productions_from_beta(self, current_non_terminal, production_number):
        """
        Eliminate productions from input stack produced by last non-terminal added to working stack
        :param current_non_terminal:
        :param production_number:
        """
        current_production_in_beta = self.grammar.getProductionsFor(current_non_terminal)[production_number]
        j = 0
        while j < len(current_production_in_beta) and self.beta.pop() == current_production_in_beta[j]:
            j += 1

    def descending_recursive_parsing(self):
        self.grammar.solveLeftRecursivity()

        while self.state != FINAL_STATE and self.state != ERROR_STATE:
            # maybe print it better
            self.f.write(f'({self.state}, {self.i}, {self.alpha}, {self.beta} )')
            #print(f'({self.state}, {self.i}, {self.alpha}, {self.beta} )', end="")
            if self.state == NORMAL_STATE:
                if self.i == len(self.w) and len(self.beta) == 0:
                    self.success()
                elif len(self.beta) == 0:
                    self.back()
                # head of beta (input stack) is nonterminal
                elif self.beta[-1] in self.grammar.getNonterminals():
                    self.expand()
                # head of beta is a terminal = to current symbol from input
                elif self.i < len(self.w) and (self.beta[-1] == self.w[self.i] or self.beta[-1] == EPSILON):
                    self.advance()
                else:
                    self.momentary_insuccess()
            elif self.state == BACK_STATE:
                if self.alpha[-1] in self.grammar.getTerminals():  # head of working stack is a terminal
                    self.back()
                else:  # head of working stack is a non terminal
                    self.another_try()

        if self.state == FINAL_STATE:
            print("sequence accepted")
        else:
            print("error!")

    def get_output_table(self, output_file_name):
        return TableOutput(self.alpha, self.grammar, output_file_name)
