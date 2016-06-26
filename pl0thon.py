
import fileinput



reserved = set(['end', 'const', 'var', 'procedure', 'begin', 'if', 'while', 'then', 'do', 'call', 'odd'])

class Reader(object):
    def __init__(self, code):
        self.code = code
        self.index = 0

    def ignore_whitespace(self):
        while self.index < len(self.code) and self.peek().isspace():
            self.forward()
            print self.index

    def peek(self):
        return self.code[self.index]

    def forward(self):
        self.index += 1

    def get_range(self, from_index, to_index):
        return self.code[from_index:to_index]

    def has_next(self):
        self.ignore_whitespace()
        return self.index < len(self.code)

class TokenType():

    IDENTIFIER = 0
    NUMBER = 1

    COMMA = 100
    SEMICOLON = 101
    BANG = 102
    QMARK = 103
    FULL_STOP = 104

    EQUALS = 300
    ASSIGNMENT = 301

    MULT = 400
    DIV = 401
    PLUS = 402
    MINUS = 403

    LT = 500
    LT_EQ = 501

    GT = 600
    GT_EQ = 601

    PAREN_OPEN = 700
    PAREN_CLOSE = 701

    RESERVED = 999


class Token(object):
    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal

    def __repr__(self):
        return str((self.token_type, self.literal))

class Tokenizer(object):
    def __init__(self, code):
        self.reader = Reader(code)
        self.tokens = []
        self.tokenize()

    def get_tokens(self):
        return self.tokens

    def tokenize(self):
        while self.reader.has_next():
            self.reader.ignore_whitespace()
            peeked = self.reader.peek()
            if "=" == peeked:
                self.tokens.append(Token(TokenType.EQUALS, peeked))
                self.reader.forward()
            elif "," == peeked:
                self.tokens.append(Token(TokenType.COMMA, peeked))
                self.reader.forward()
            elif "?" == peeked:
                # Literally no idea what this is
                self.tokens.append(Token(TokenType.QMARK, peeked))
                self.reader.forward()
            elif "!" == peeked:
                self.tokens.append(Token(TokenType.BANG, peeked))
                self.reader.forward()
            elif ";" == peeked:
                self.tokens.append(Token(TokenType.SEMICOLON, peeked))
                self.reader.forward()
            elif "+" == peeked:
                self.tokens.append(Token(TokenType.PLUS, peeked))
                self.reader.forward()
            elif "-" == peeked:
                self.tokens.append(Token(TokenType.MINUS, peeked))
                self.reader.forward()
            elif "*" == peeked:
                self.tokens.append(Token(TokenType.MULT, peeked))
                self.reader.forward()
            elif "/" == peeked:
                self.tokens.append(Token(TokenType.DIV, peeked))
                self.reader.forward()
            elif "{" == peeked:
                self.tokens.append(Token(TokenType.PAREN_OPEN, peeked))
                self.reader.forward()
            elif "}" == peeked:
                self.tokens.append(Token(TokenType.PAREN_CLOSE, peeked))
                self.reader.forward()
            elif "." == peeked:
                self.tokens.append(Token(TokenType.FULL_STOP, peeked))
                self.reader.forward()
            elif ":" == peeked:
                self.reader.forward()
                if not self.reader.peek() == "=":
                    raise Exception()
                self.tokens.append(Token(TokenType.ASSIGNMENT, ":="))
                self.reader.forward()
            elif "<" == peeked:
                self.reader.forward()
                if not self.reader.peek() == "=":
                    self.tokens.append(Token(TokenType.LT_EQ, "<="))
                    self.reader.forward()
                else:
                    self.tokens.append(Token(TokenType.LT, "<"))
            elif ">" == peeked:
                self.reader.forward()
                if not self.reader.peek() == "=":
                    self.tokens.append(Token(TokenType.GT_EQ, "<="))
                    self.reader.forward()
                else:
                    self.tokens.append(Token(TokenType.GT, "<"))
            elif peeked.isdigit():
                self.tokens.append(Token(TokenType.NUMBER, self.parse_number()))
            elif peeked.isalpha():
                identifier = self.parse_identifier()
                if identifier.lower() in reserved:
                    self.tokens.append(Token(TokenType.RESERVED, identifier))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier))
            else:
                print "UNHANDLED CASE", peeked

            print self.tokens

    def parse_identifier(self):
        start_index = self.reader.index
        if not self.reader.peek().isalpha():
            raise Exception()
        while self.reader.peek().isalnum():
            self.reader.forward()
        end_index = self.reader.index
        return self.reader.get_range(start_index, end_index)

    def parse_number(self):
        start_index = self.reader.index
        if not self.reader.peek().isdigit():
            raise Exception()
        while self.reader.peek().isdigit():
            self.reader.forward()
        end_index = self.reader.index
        return self.reader.get_range(start_index, end_index)


# class Parser(object):
    # def __init__(self, tokens):
        # self.tokens = tokens
        # self.index = 0

    # def produce_tokens(self):
        # self.program()
        # self.expect('.')

    # def expect(self, expected):
        # if not self.tokens[self.index][1] == expected:
            # raise Exception()

    # def optional(self, value)
        # return self.tokens[self.index][1] == expected:

    # def program(self):
        # self.block()
        # self.expect('.')

    # def block(self):
        # if self.optional('const'):
            # pass


program = "".join([line for line in fileinput.input()])
tokenizer = Tokenizer(program)
parser = Parser(tokenizer.get_tokens())
