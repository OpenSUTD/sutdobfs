import unittest
import random
from sutdobfs.providers import ConsistentProvider


class MyTestCase(unittest.TestCase):
    def test_same_word_gives_same_hash(self):
        memes = ["a", "e", "i", "o", "u"]
        p1 = ConsistentProvider(memes)
        p2 = ConsistentProvider(memes)
        self.assertEqual(p1.meme("hello"), p2.meme("hello"))
        self.assertEqual(p1.meme("hello"), p1.meme("hello"))

    def test_hash_collision_will_result_in_copy(self):
        memes = ["a", "e", "i", "o", "u"]
        p1 = ConsistentProvider(memes)
        s1 = str(random.random())
        m1 = p1.meme(s1)
        # try to find another string with a colliding name
        s2 = None
        m2 = None
        while m1 != m2:
            s2 = str(random.random())
            p2 = ConsistentProvider(memes)
            m2 = p2.meme(s2)
        m2 = p1.meme(s2)
        # check that _copy is produced
        self.assertEqual(m1 + "_copy", m2)


if __name__ == "__main__":
    unittest.main()
