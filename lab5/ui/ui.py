import os

from domain.grammar import Grammar
from domain.parser import Parser


class UI:
    def printMenu(self):
        print("0. exit")
        print("1. read grammar from file")
        print("2. print set of nonterminals")
        print("3. print set of terminals")
        print("4. print set of productions")
        print("5. print productions for a given nonterminal")
        print("6. CFG check")

    def run(self):
        grammar = Grammar()
        grammar.readFromFile("g3.txt")
        parser = Parser(grammar, "x1 c c s s a")
        # grammar.readFromFile("g4.txt")
        # parser = Parser(grammar, "a b a a b b")
        parser.descending_recursive_parsing()
        parser_output = parser.get_output_table()
        parser_output.get_output_as_string()
        # while True:

            # self.printMenu()
            # command = input("command: ")
            # if command == "0":
            #     break
            # elif command == "1":
            #     file = input("file: ")
            #     if os.path.isfile(file):
            #         grammar.readFromFile(file)
            #     else:
            #         print("file does not exist")
            # elif command == "2":
            #     print(grammar.getNonterminals())
            # elif command == "3":
            #     print(grammar.getTerminals())
            # elif command == "4":
            #     print(grammar.getProductions())
            # elif command == "5":
            #     nonterminal = input("nonterminal: ")
            #     print(grammar.getProductionsFor(nonterminal))
            # elif command == "6":
            #     print(grammar.CFGCheck())

