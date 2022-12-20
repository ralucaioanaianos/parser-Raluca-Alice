from tabulate import tabulate

from domain.Node import Node


class TableOutput:
    def __init__(self, alpha, grammar, output_file_name):
        self.alpha = alpha  # working stack
        self.grammar = grammar
        self.output_file_name = output_file_name

    def get_output_as_string(self):
        productions = list(
            filter(lambda production: production.split(" ")[0] in self.grammar.getNonterminals(), self.alpha))

        if len(productions) > 0:
            first_production = productions[0]
            first_non_terminal = first_production.split(" ")[0]
            production_number = int(first_production.split(" ")[1])
            first_rule = self.grammar.getProductionsFor(first_non_terminal)[production_number]

            root = Node(first_non_terminal)

            root.child = self.build_tree(first_rule, productions)

            rows = self.bfs(root)

            rows.insert(0, ['index', 'info', 'parent', 'right_sibling'])
            f = open(self.output_file_name, "w")
            f.write(tabulate(rows, headers='firstrow'))

    def build_tree(self, rule, productions):
        """
        Build the graph based on the starting rule and the non terminals from the working stack (alpha)
        - if it is terminal then it has a right sibling but no child
        :param rule:
        :param productions:
        :return:
        """
        if len(rule) == 0:
            return

        symbol = rule[0]
        # if it is terminal then it has a right sibling but no child
        if symbol in self.grammar.getTerminals():
            node = Node(symbol)
            node.right_sibling = self.build_tree(rule[1:], productions)
            return node
        # if it is a nonterminal then it can have both a child and a right sibling
        elif symbol in self.grammar.getNonterminals():
            node = Node(symbol)
            productions.pop(0)  # you finished with the current non terminal from the working stack, go to the next one
            first_production = productions[0]
            first_non_terminal = first_production.split(" ")[0]
            production_number = int(first_production.split(" ")[1])
            first_rule = self.grammar.getProductionsFor(first_non_terminal)[production_number]
            node.child = self.build_tree(first_rule, productions)
            node.right_sibling = self.build_tree(rule[1:], productions)
            return node
        else:
            return Node("epsilon")

    def bfs(self, root):
        # Create a queue for BFS
        queue = [root]
        traversal = []
        parent_of = {}
        sibling_of = {}
        current_index = 1

        while queue:
            # Dequeue a vertex from queue
            node = queue.pop(0)
            node.index = current_index
            current_index += 1
            traversal.append(node)
            current_sibling = node
            right_sibling = node.right_sibling
            while right_sibling is not None:
                if right_sibling not in queue:
                    queue.append(right_sibling)
                    parent_of[right_sibling] = parent_of[node]  # save the parent of the right sibling as the parent of the current node
                    sibling_of[right_sibling] = current_sibling  # save this node as the right sibling of the current node
                current_sibling = right_sibling
                right_sibling = right_sibling.right_sibling

            if node.child is not None:
                # save the current node as the parent of its child
                queue.append(node.child)
                parent_of[node.child] = node

        # for pretty print
        rows = []
        for i in range(0, len(traversal)):
            node = traversal[i]

            index = str(i+1)
            info = node.value

            parent = 0
            if node in parent_of:
                parent = parent_of[node].index

            right_sibling = 0
            if node in sibling_of:
                right_sibling = sibling_of[node].index

            rows.append([index, info, parent, right_sibling])

        return rows
