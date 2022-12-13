import uuid


class Node:
    def __init__(self, value):
        self.uuid = uuid.uuid1(node=None, clock_seq=None)
        self.value = value
        self.child = None
        self.right_sibling = None
        self.index = None
