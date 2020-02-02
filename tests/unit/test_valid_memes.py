import unittest
import keyword
import os
import glob
import sys
import sutdobfs


class MyTestCase(unittest.TestCase):
    def test_all_memes_are_valid_replacement_names(self):
        # sys.path.insert(0, "../../sutdobfs")
        d = os.path.dirname(sys.modules["sutdobfs"].__file__)
        meme_file_paths = glob.glob(os.path.join(d, "memes", "*.txt"))
        for meme_file_path in meme_file_paths:
            meme_file = open(meme_file_path)
            for meme in [m.rstrip() for m in meme_file.readlines()]:
                if not meme.startswith("#") and len(meme) != 0:
                    self.assertTrue(meme.isidentifier())
                    self.assertFalse(keyword.iskeyword(meme))
                    self.assertTrue(meme not in __builtins__)
            meme_file.close()
