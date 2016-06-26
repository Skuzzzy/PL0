
import fileinput
import time



reserved = set(['end', 'const', 'var', 'procedure', 'begin', 'if', 'while', 'then', 'do', 'call', 'odd'])

class Reader(object):
    def __init__(self, code):
        self.code = code
        self.index = 0

    def ignore_whitespace(self):
        while self.index < len(self.code) and self.peek().isspace():
            self.forward()
            # print self.index

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
            if '=' == peeked:
                self.tokens.append(Token(TokenType.EQUALS, peeked))
                self.reader.forward()
            elif ',' == peeked:
                self.tokens.append(Token(TokenType.COMMA, peeked))
                self.reader.forward()
            elif '?' == peeked:
                # Literally no idea what this is
                self.tokens.append(Token(TokenType.QMARK, peeked))
                self.reader.forward()
            elif '!' == peeked:
                self.tokens.append(Token(TokenType.BANG, peeked))
                self.reader.forward()
            elif ';' == peeked:
                self.tokens.append(Token(TokenType.SEMICOLON, peeked))
                self.reader.forward()
            elif '+' == peeked:
                self.tokens.append(Token(TokenType.PLUS, peeked))
                self.reader.forward()
            elif '-' == peeked:
                self.tokens.append(Token(TokenType.MINUS, peeked))
                self.reader.forward()
            elif '*' == peeked:
                self.tokens.append(Token(TokenType.MULT, peeked))
                self.reader.forward()
            elif '/' == peeked:
                self.tokens.append(Token(TokenType.DIV, peeked))
                self.reader.forward()
            elif '{' == peeked:
                self.tokens.append(Token(TokenType.PAREN_OPEN, peeked))
                self.reader.forward()
            elif '}' == peeked:
                self.tokens.append(Token(TokenType.PAREN_CLOSE, peeked))
                self.reader.forward()
            elif '.' == peeked:
                self.tokens.append(Token(TokenType.FULL_STOP, peeked))
                self.reader.forward()
            elif ':' == peeked:
                self.reader.forward()
                if not self.reader.peek() == '=':
                    raise Exception()
                self.tokens.append(Token(TokenType.ASSIGNMENT, ':='))
                self.reader.forward()
            elif '<' == peeked:
                self.reader.forward()
                if self.reader.peek() == '=':
                    self.tokens.append(Token(TokenType.LT_EQ, '<='))
                    self.reader.forward()
                else:
                    self.tokens.append(Token(TokenType.LT, '<'))
            elif '>' == peeked:
                self.reader.forward()
                if self.reader.peek() == '=':
                    self.tokens.append(Token(TokenType.GT_EQ, '<='))
                    self.reader.forward()
                else:
                    self.tokens.append(Token(TokenType.GT, '<'))
            elif peeked.isdigit():
                self.tokens.append(Token(TokenType.NUMBER, self.parse_number()))
            elif peeked.isalpha():
                identifier = self.parse_identifier()
                if identifier.lower() in reserved:
                    self.tokens.append(Token(TokenType.RESERVED, identifier))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier))
            else:
                print 'UNHANDLED CASE', ord(peeked)
                self.reader.forward()
                time.sleep(1)

            # print self.tokens

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


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0


        print "\n".join([str(x) for x in self.tokens])
        print self.program()

    def debug(self):
        print self.index
        print self.tokens[self.index]

    def produce_tokens(self):
        self.program()
        self.expect('.')

    def expect(self, expected):
        token = self.tokens[self.index]
        if not token.literal.lower() == expected:
            raise Exception()
        self.index += 1
        return token

    def expect_type(self, expected_type):
        token = self.tokens[self.index]
        if not token.token_type == expected_type:
            raise Exception()
        self.index += 1
        return token

    def optional(self, value, consume=True):
        option = self.tokens[self.index].literal.lower() == value
        if option and consume:
            self.index += 1
        return option

    def optional_type(self, value, consume=True):
        option = self.tokens[self.index].token_type == value
        if option and consume:
            self.index += 1
        return option

    def program(self):
        blok = self.block()
        self.expect('.')
        return blok

    def block(self):
        consts = []
        if self.optional('const'):
            ident = self.expect_type(TokenType.IDENTIFIER)
            self.expect('=')
            number = self.expect_type(TokenType.NUMBER)
            consts.append((ident, number))
            while self.optional(','):
                ident = self.expect_type(TokenType.IDENTIFIER)
                self.expect('=')
                number = self.expect_type(TokenType.NUMBER)
                consts.append((ident, number))
            self.expect(';')
        variables = []
        if self.optional('var'):
            ident = self.expect_type(TokenType.IDENTIFIER)
            variables.append(ident)
            while self.optional(','):
                ident = self.expect_type(TokenType.IDENTIFIER)
                variables.append(ident)
            self.expect(';')

        procedures = []
        while self.optional('procedure'):
            ident = self.expect_type(TokenType.IDENTIFIER)
            self.expect(';')
            subblock = self.block()
            self.expect(';')
            procedures.append((ident, subblock))
        stmnt = self.statement()
        return (consts, variables, procedures, stmnt)

    def statement(self):
        if self.optional_type(TokenType.IDENTIFIER, consume=False):
            ident = self.expect_type(TokenType.IDENTIFIER)
            self.debug()
            assign = self.expect_type(TokenType.ASSIGNMENT)
            expr = self.expression()
            return (assign, ident, expr)
        elif self.optional('call', consume=False):
            call = self.expect('call')
            ident = self.expect_type(TokenType.IDENTIFIER)
            return (call, ident)
        elif self.optional('?'):
            ident = self.expect_type(TokenType.IDENTIFIER)
            return ('?', ident)
        elif self.optional('!'):
            expr = self.expression()
            return ('!', expr)
        elif self.optional('begin'):
            statements = []
            stmnt = self.statement()
            statements.append(stmnt)
            while self.optional(';'):
                stmnt = self.statement()
                statements.append(stmnt)
            self.expect('end')
            return ('statements', statements)
        elif self.optional('if'):
            cond = self.condition()
            self.expect('then')
            stmnt = self.statement()
            return ('if', cond, stmnt)
        elif self.optional('while'):
            cond = self.condition()
            self.expect('do')
            stmnt = self.statement()
            return ('while', cond, stmnt)
        else:
            self.debug()
            raise Exception()

    def condition(self):
        if self.optional('odd'):
            expr = self.expression()
            return ('odd', expr)
        else:
            first_expr = self.expression()

            # FIXME Lazy Hack
            cmp_op = self.tokens[self.index]
            self.index += 1

            second_expr = self.expression()

            return (first_expr, cmp_op, second_expr)

    def is_plus_minus(self):
        return self.tokens[self.index].literal in set(['+', '-'])

    def is_minus(self):
        boolean = self.tokens[self.index].literal == '+'
        self.index += 1
        return boolean

    def expression(self):
        termpairs = []
        sign = '+'
        if self.is_plus_minus():
            if self.is_minus():
                sign = '-'
        term = self.term()
        termpairs.append((sign, term))
        while self.is_plus_minus():
            sign = '+' # Everything is implicit positive num
            # FIXME Implicitely assumes addition
            if self.is_minus():
                sign = '-'
            term = self.term()
            termpairs.append((sign, term))
        return termpairs

    def is_mult_div(self):
        return self.tokens[self.index].literal in set(['*', '/'])

    def is_div(self):
        boolean = self.tokens[self.index].literal == '/'
        self.index += 1
        return boolean

    def term(self):
        factorlist = []
        factor = self.factor()
        factorlist.append(factor)
        while self.is_mult_div():
            operation = "*"
            # FIXME Implicitely assumes multiplication
            if self.is_div():
                operation = "/"

            factor = self.factor()
            factorlist.append((operation, factor))
        return factorlist

    def factor(self):
        if self.optional_type(TokenType.IDENTIFIER, consume=False):
            factor = self.expect_type(TokenType.IDENTIFIER)
            return factor
        elif self.optional_type(TokenType.NUMBER, consume=False):
            factor = self.expect_type(TokenType.NUMBER)
            return factor
        else:
            self.debug()
            self.expect('(')
            expr = self.expression()
            self.expect(')')
            return expr

program = ''.join([line for line in fileinput.input()])
tokenizer = Tokenizer(program)
parser = Parser(tokenizer.get_tokens())
