class LookupTable:
    class Node:
        def __init__(self, name):
            self.name = name
            self.next = None

    def __init__(self, hash_function: callable, memes: list):
        self.__name_table = dict()
        self.__meme_table = dict(enumerate(memes))
        self.__hash = hash_function

    def __getitem__(self, name: str):
        if type(name) is not str:
            raise TypeError(f"Expected str for name, got {type(name)}")
        h = self.__hash(name)
        if h in self.__name_table:
            node = self.__name_table[h]
            depth = 0
            while node.next is not None and node.name != name:
                node = node.next
                depth += 1
            if node.next is None and node.name != name:
                return self.__init_item(name) + "_copy" * (depth + 1)
            if h not in self.__meme_table:
                raise IndexError(f"Index {h} does not exist in Meme Lookup Table")
            return self.__meme_table[h] + "_copy" * depth
        else:
            return self.__init_item(name)

    def __init_item(self, name: str):
        h = self.__hash(name)
        if h in self.__name_table:
            node = self.__name_table[h]
            depth = 0
            while node.next is not None and node.name != name:
                node = node.next
                depth += 1
            if node.name == name:
                return
            elif node.next is None:
                node.next = self.__class__.Node(name)
            else:
                raise LookupError("Illegal state")
        else:
            self.__name_table[h] = self.__class__.Node(name)
        return self.__meme_table[h]
