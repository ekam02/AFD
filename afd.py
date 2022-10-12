import re
from random import Random


class Node:
    @classmethod
    def is_name(cls, name) -> bool:
        return True if re.search('q[0-9]+', name) else False

    @classmethod
    def _name(cls, name) -> str:
        return name if cls.is_name(name) else ''

    @classmethod
    def is_status(cls, status) -> bool:
        return bool(status) if isinstance(status, bool) or status in (0, 1) else False

    @classmethod
    def is_symbol(cls, symbol) -> bool:
        if isinstance(symbol, str) and len(symbol) == 1 and bool(re.search('[0-9a-zA-Z]', symbol)):
            return True
        else:
            return False

    @classmethod
    def is_edge(cls, edge: dict) -> bool:
        if isinstance(edge, dict) and len(edge) == 1:
            key, value = tuple(edge.items())[0]
            return True if cls.is_symbol(key) and cls.is_name(value) else False
        else:
            return False

    @classmethod
    def _edges(cls, edges: dict) -> dict:
        return {symbol: name for symbol, name in edges.items() if cls.is_edge({symbol: name})}

    def __init__(self, *args, **kwargs):
        self.__name, self.__status, self.__main, self.__edges = '', False, False, {}

        if args:
            if len(args) > 0:
                self.__name = self._name(args[0])

            if len(args) > 1:
                self.__status = self.is_status(args[1])

            if len(args) > 2:
                self.__main = self.is_status(args[2])

            if len(args) > 3:
                self.__edges = self._edges(args[3])

        if kwargs:
            if 'name' in kwargs:
                self.__name = self._name(kwargs['name'])

            if 'status' in kwargs:
                self.__status = self.is_status(kwargs['status'])

            if 'main' in kwargs:
                self.__status = self.is_status(kwargs['main'])

            if 'edges' in kwargs:
                self.__edges = self._edges(kwargs['edges'])

            self.__edges.update(self._edges(kwargs))

    @property
    def name(self) -> str:
        return f'*{self.__name}' if self.__status else f'*{self.__name}'

    @name.setter
    def name(self, name: str):
        self.__name = self._name(name)

    @property
    def status(self) -> bool:
        return self.__status

    @status.setter
    def status(self, status: bool):
        self.__status = self.is_status(status)

    @property
    def main(self) -> bool:
        return self.__main

    @main.setter
    def main(self, main):
        self.__main = self.is_status(main)

    @property
    def edges(self) -> dict:
        return self.__edges

    @edges.setter
    def edges(self, edges: dict):
        self.__edges = self._edges(edges)

    def edge(self, edge: dict):
        self.__edges.update(self._edges(edge))

    def transition(self, symbol) -> str:
        return self.__edges[symbol] if symbol in self.__edges else None

    @property
    def info(self) -> dict:
        return {'name': self.__name, 'status': self.__status, 'edges': self.__edges}

    def __str__(self) -> str:
        return self.name


class Bot:
    @classmethod
    def regex(cls, alphabet: list) -> list:
        alphabet = list(filter(lambda item: isinstance(item, str) and 0 < len(item) < 2, alphabet))
        alphabet = list(filter(lambda character: bool(re.search('[0-9a-zA-z]', character)), alphabet))
        alphabet = dict(zip(alphabet, alphabet))
        return list(alphabet.keys())

    @classmethod
    def make_nodes(cls, nodes: int) -> list:
        return [Node(f'q{i}') for i in range(nodes)] if nodes > 1 else [Node('q0')]

    def __init__(self, *args, **kwargs):
        self.__nodes, self.__alphabet = [], []

        if args:
            if len(args) > 0 and isinstance(args[0], int):
                self.__nodes = self.make_nodes(args[0])

            if len(args) > 1 and isinstance(args[1], (str, list, tuple)):
                self.__alphabet = self.regex(list(args[1]))

        if kwargs:
            if 'nodes' in kwargs and isinstance(kwargs['nodes'], int):
                self.__nodes = self.make_nodes(kwargs['nodes'])

            if 'alphabet' in kwargs and isinstance(kwargs['alphabet'], (str, list, tuple)):
                self.__alphabet = self.regex(list(kwargs['alphabet']))

    @property
    def nodes(self) -> list:
        return self.__nodes

    @property
    def alphabet(self) -> list:
        return self.__alphabet

    @alphabet.setter
    def alphabet(self, alphabet: str):
        self.__alphabet = self.regex(list(alphabet))

    @property
    def initial_state(self) -> str:
        return self.__nodes[0].name if self.__nodes else ''

    @property
    def final_states(self) -> list:
        return [node.name for node in self.__nodes if node.status] if self.__nodes else []

    @property
    def info(self) -> dict:
        return {'alphabet': self.__alphabet, 'nodes': [node.info for node in self.__nodes]}

    def extended_transition(self, word: list) -> tuple:
        iterator, result, word = self.__nodes[0], list(), list(word)
        for i in word:
            next_node = iterator.transition(i)
            result.append(f"d({iterator.name}, '{i}') = {next_node.name if next_node else None}")
            iterator = next_node if next_node else iterator
        return result, iterator.status

    def __str__(self) -> str:
        return f"alphabet: {self.__alphabet}, nodes: {[node.name for node in self.__nodes]}"
