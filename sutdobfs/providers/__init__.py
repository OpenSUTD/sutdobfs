import hashlib
from .utils import LookupTable


class Provider:
    def meme(self, name: str) -> str:
        pass


class ConsistentProvider(Provider):
    """
    This provider will assign memes based on the name of the identifier and nothing else.
    """

    def __init__(self, available_memes: list):
        self.__lookup_table = LookupTable(self.__hash, available_memes)
        self.__available_memes = available_memes

    def __hash(self, name: str) -> int:
        return int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16) % len(
            self.__available_memes
        )

    def meme(self, name: str) -> str:
        return self.__lookup_table[name]
