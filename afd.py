import re


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
    def is_vertex(cls, vertex: dict) -> bool:
        if isinstance(vertex, dict) and len(vertex) == 1:
            key, value = tuple(vertex.items())[0]
            return True if cls.is_symbol(key) and cls.is_name(value) else False
        else:
            return False

    @classmethod
    def _vertexes(cls, vertexes: dict) -> dict:
        return {symbol: name for symbol, name in vertexes.items() if cls.is_vertex({symbol: name})}

    def __init__(self, *args, **kwargs):
        self.__name, self.__status, self.__vertexes = '', False, {}

        if args:
            if len(args) > 0:
                self.__name = self._name(args[0])

            if len(args) > 1:
                self.__status = self.is_status(args[1])

            if len(args) > 2:
                self.__vertexes = self._vertexes(args[2])

        if kwargs:
            if 'name' in kwargs:
                self.__name = self._name(kwargs['name'])

            if 'status' in kwargs:
                self.__status = self.is_status(kwargs['status'])

            if 'vertexes' in kwargs:
                self.__vertexes = self._vertexes(kwargs['vertexes'])

            self.__vertexes.update(self._vertexes(kwargs))

    @property
    def name(self) -> str:
        return self.__name

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
    def vertexes(self) -> dict:
        return self.__vertexes

    @vertexes.setter
    def vertexes(self, vertexes: dict):
        self.__vertexes = self._vertexes(vertexes)

    def transition(self, symbol) -> str:
        return self.__vertexes[symbol] if symbol in self.__vertexes else None

    @property
    def info(self) -> dict:
        return {'name': self.__name, 'status': self.__status, 'vertexes': self.__vertexes}

    def __str__(self) -> str:
        return self.__name


class Bot:
    @classmethod
    def regex(cls, alphabet: list) -> list:
        try:
            alphabet = list(filter(lambda item: isinstance(item, str) and 0 < len(item) < 2, alphabet))
            alphabet = list(filter(lambda character: bool(re.search('[0-9a-zA-z]', character)), alphabet))
            alphabet = dict(zip(alphabet, alphabet))
            return list(alphabet.keys())
        except:
            return list()

    def __init__(self, *args, **kwargs):
        self.__nodes, self.__alphabet = {}, {}

        if args:
            if len(args) > 0 and isinstance(args[0], int):
                self.__nodes = {f'q{i}': Node(f'q{i}') for i in range(args[0])} if args[0] > 1 else {'q0': Node('q0')}

            if len(args) > 1 and isinstance(args[1], (str, list, tuple)):
                self.__alphabet = self.regex(list(args[1]))

        if kwargs:
            pass

    @property
    def nodes(self) -> dict:
        return self.__nodes

    @property
    def alphabet(self) -> list:
        return self.__alphabet

    @property
    def initial_state(self) -> str:
        return self.__nodes['q0'].name if self.__nodes else ''

    @property
    def final_states(self) -> dict:
        return [node.name for key, node in self.__nodes.items() if node.status] if self.__nodes else {}

    # TODO
    @property
    def info(self) -> dict:
        pass

    def extended_transition(self, word: list) -> tuple:
        iterator, result, word = self.__nodes['q0'], list(), list(word)
        for i in word:
            next_node = self.nodes[iterator.transition(i)]
            result.append(f'd({iterator.name}, \'{i}\') = {next_node.name if next_node else None}')
            iterator = next_node if next_node else iterator
        return result, iterator.status

    def __str__(self) -> str:
        pass


if __name__ == '__main__':
    bot = Bot(5, 'bacd')
    bot.nodes['q0'].status = 1
    bot.nodes['q2'].status = 1
    bot.nodes['q4'].status = 1

    bot.nodes['q0'].vertexes = {'b': 'q1', 'c': 'q3', 'd': 'q4'}
    bot.nodes['q1'].vertexes = {'a': 'q2'}
    bot.nodes['q2'].vertexes = {'b': 'q1', 'c': 'q3', 'd': 'q4'}
    bot.nodes['q3'].vertexes = {'c': 'q3', 'd': 'q4'}
    bot.nodes['q4'].vertexes = {'c': 'q3', 'd': 'q4'}

    word = list('babacccdcccd')
    steps, validation = bot.extended_transition(word)
    print(steps, validation)
