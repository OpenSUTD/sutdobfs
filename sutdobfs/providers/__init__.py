import hashlib


class Provider:
    def meme(self, name):
        pass


class ConsistentProvider(Provider):
    """
    This provider will assign memes based on the name of the identifier and nothing else.
    """

    class LinkedNode:
        def __init__(self, name, meme):
            self.name = name
            self.meme = meme
            self.__next = None
            self.prev = None

        def __set_next(self, next):
            self.__next = next
            next.prev = self

        def __get_next(self):
            return self.__next

        def __get_depth(self):
            depth = 0
            prev = self.prev
            while prev is not None:
                depth += 1
                prev = prev.prev
            return depth

        next = property(__get_next, __set_next)
        depth = property(__get_depth)

    def __init__(self, available_memes):
        self.__hash_table = dict()
        self.__available_memes = available_memes

    def __hash(self, name) -> int:
        return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) % len(
            self.__available_memes
        )

    def meme(self, name):
        k = self.__hash(name)
        if k in self.__hash_table:
            n = self.__hash_table[k]
            while n.name != name and n.next is not None:
                n = n.next
            if n.name != name:
                n.next = ConsistentProvider.LinkedNode(name, self.__available_memes[k])
                n = n.next
            return n.meme + ("_copy" * n.depth)
        else:
            self.__hash_table[k] = ConsistentProvider.LinkedNode(
                name, self.__available_memes[k]
            )
            return self.__hash_table[k].meme
