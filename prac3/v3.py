import re

NUM_OF_KWORDS = 2
keywords = ["for", "do"]

class TokenNames:
    KWORD = 'KWORD'
    IDENT = 'IDENT'
    NUM = 'NUM'
    OPER = 'OPER'
    DELIM = 'DELIM'

class States:
    H = 'H'
    ID = 'ID'
    NM = 'NM'
    ASGN = 'ASGN'
    DLM = 'DLM'
    ERR = 'ERR'
class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value

class LexemeTable:
    def __init__(self, tok):
        self.tok = tok
        self.next = None

lt = None
lt_head = None

def lexer(filename):
    try:
        with open(filename, 'r') as file:
            c = file.read(1)
            CS = States.H
            while c:
                if CS == States.H:
                    while c == ' ' or c == '\t' or c == '\n':
                        c = file.read(1)
                    if c.isalpha() or c == '_':
                        CS = States.ID
                    elif c.isdigit() or c == '.' or c == '+' or c == '-':
                        CS = States.NM
                    elif c == ':':
                        CS = States.ASGN
                    else:
                        CS = States.DLM
                elif CS == States.ASGN:
                    colon = c
                    c = file.read(1)
                    if c == '=':
                        tok = Token(TokenNames.OPER, ':=')
                        add_token(tok)
                        c = file.read(1)
                        CS = States.H
                    else:
                        err_symbol = colon
                        CS = States.ERR
                elif CS == States.DLM:
                    if c == '(' or c == ')' or c == ';':
                        tok = Token(TokenNames.DELIM, c)
                        add_token(tok)
                        c = file.read(1)
                        CS = States.H
                    elif c == '<' or c == '>' or c == '=':
                        tok = Token(TokenNames.OPER, c)
                        add_token(tok)
                        c = file.read(1)
                        CS = States.H
                    else:
                        err_symbol = c
                        c = file.read(1)
                        CS = States.ERR
                elif CS == States.ERR:
                    print(f"Unknown character: {err_symbol}")
                    CS = States.H
                elif CS == States.ID:
                    buf = c
                    c = file.read(1)
                    while c.isalnum() or c == '_':
                        buf += c
                        c = file.read(1)
                    if is_kword(buf):
                        tok = Token(TokenNames.KWORD, buf)
                    else:
                        tok = Token(TokenNames.IDENT, buf)
                    add_token(tok)
                    CS = States.H
                elif CS == States.NM:
                    buf = c
                    c = file.read(1)
                    while c.isdigit() or c == '.':
                        buf += c
                        c = file.read(1)
                    tok = Token(TokenNames.NUM, buf)
                    add_token(tok)
                    CS = States.H
    except IOError:
        print(f"Cannot open file {filename}")
        return -1

def is_kword(string):
    return string in keywords

def add_token(tok):
    global lt, lt_head
    lexeme = LexemeTable(tok)
    if lt is None:
        lt = lexeme
        lt_head = lexeme
    else:
        lt.next = lexeme
        lt = lexeme
    print("Token created - name:", tok.token_name, "value:", tok.token_value)


lexer("C://Users//artez//Desktop//example.txt")  # Replace 'input.txt' with the actual filename