import hashlib
import random
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


class RandomConsistentProvider(Provider):
    """
    This provider will assign a random meme based on the name of the identifier. It is consistent because the same name in the same session will always result in the same meme.
    """

    def __init__(self, available_memes: list):
        self.__lookup_table = LookupTable(self.__hash, available_memes)
        self.__available_memes = available_memes
        self.__name_to_hash_number = dict()

    def __hash(self, name: str) -> int:
        if name in self.__name_to_hash_number:
            return self.__name_to_hash_number[name]
        else:
            h = random.randrange(len(self.__available_memes))
            self.__name_to_hash_number[name] = h
            return h

    def meme(self, name: str) -> str:
        return self.__lookup_table[name]


class SequentialProvider(Provider):
    """
    This provider will assign memes based on the order it encounters names in the source code. This provider ensures that all names in the meme dictionary will be used if there are more unique names than entries in the meme dictionary.
    """

    def __init__(self, available_memes: list):
        self.__lookup_table = LookupTable(self.__hash, available_memes)
        self.__available_memes = available_memes
        self.__name_to_hash_number = dict()

    def __hash(self, name: str) -> int:
        if name in self.__name_to_hash_number:
            return self.__name_to_hash_number[name]
        else:
            h = len(self.__name_to_hash_number)
            self.__name_to_hash_number[name] = h
            return h

    def meme(self, name: str) -> str:
        return self.__lookup_table[name]


class RandomSequentialProvider(Provider):
    """
    This provider will assign memes based on the randomised order it encounters names in the source code. This provider ensures that all names in the meme dictionary will be used if there are more unique names than entries in the meme dictionary.
    """

    def __init__(self, available_memes: list):
        self.__lookup_table = LookupTable(self.__hash, available_memes)
        self.__available_memes = available_memes
        self.__name_to_hash_number = dict()

    def __hash(self, name: str) -> int:
        if name in self.__name_to_hash_number:
            return self.__name_to_hash_number[name]
        else:
            unused_numbers = set(range(len(self.__available_memes))) - set(
                self.__name_to_hash_number.values()
            )
            if len(unused_numbers) != 0:
                h = random.sample(unused_numbers, 1)[0]
                self.__name_to_hash_number[name] = h
                return h
            else:
                # no more unused numbers, just random
                h = random.randrange(len(self.__available_memes))
                self.__name_to_hash_number[name] = h
                return h

    def meme(self, name: str) -> str:
        return self.__lookup_table[name]
