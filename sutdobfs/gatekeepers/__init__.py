import keyword
import tokenize


class SafeGatekeeper:
    """
  This class will only meme non-member identifiers in the Local and Enclosed scopes
  """

    def __init__(self):
        self.__scope_state = "global"
        self.__member_state = "nonmember"
        self.globals = []
        self.indent_count = 0

    def read(self, token):
        # first handle scope state transitions
        if self.__scope_state == "global":
            if token.type == tokenize.NAME and token.string == "def":
                self.__scope_state = "def"
        elif self.__scope_state == "def":
            if token.type == tokenize.OP and token.string == ":":
                self.__scope_state = ":"
        elif self.__scope_state == ":":
            if token.type == tokenize.NEWLINE:
                self.__scope_state = "local"
            else:
                self.__scope_state = "def"
        elif self.__scope_state == "local":
            if token.type == tokenize.INDENT:
                self.indent_count += 1
            elif token.type == tokenize.DEDENT:
                self.indent_count -= 1
                if self.indent_count <= 0:
                    self.__scope_state = "global"
                    self.indent_count = 0
        # next handle member/nonmember state transitions
        if self.__member_state == "nonmember":
            if token.type == tokenize.OP and token.string == ".":
                self.__member_state = "member"
        elif self.__member_state == "member":
            if token.type == tokenize.NAME:
                self.__member_state = "member"
            elif token.type == tokenize.OP and token.string == ".":
                self.__member_state = "member"
            else:
                self.__member_state = "nonmember"
        # register globals
        if self.__scope_state != "local":
            if token.type == tokenize.NAME:
                if str.isidentifier(token.string) and not keyword.iskeyword(
                    token.string
                ):
                    self.globals.append(token.string)
        # then handle output
        if self.__scope_state != "local" or self.__member_state != "nonmember":
            return False
        if (
            token.type == tokenize.NAME
            and str.isidentifier(token.string)
            and not keyword.iskeyword(token.string)
            and token.string not in __builtins__
            and token.string not in self.globals
        ):
            return True
        else:
            return False
