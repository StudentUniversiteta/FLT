NUM_OF_KWORDS = 2
keywords = ["for", "do"]
# Объявление перечислений для состояний и типов токенов
class states:
    H = 0  # начальное состояние
    ID = 1  # идентификаторы
    NM = 2  # числа
    ASGN = 3  # Знак присваивания (:=)
    DLM = 4  # Разделители (;, (,), =, >, <)
    ERR = 5  # Нераспознанные символы

class tok_names:
    KWORD = 0
    IDENT = 1
    NUM = 2
    OPER = 3
    DELIM = 4

# Определение класса для токена
class token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value

# Определение класса для таблицы лексем
class lexeme_table:
    def __init__(self, tok):
        self.tok = tok
        self.next = None

lt = None
lt_head = None

# Функция лексического анализа
def lexer(filename):
    # Открытие файла
    try:
        fd = open(filename, "r")
        print("File opened successfully.")
    except IOError:
        print("\nCannot open file {}.\n".format(filename))
        return -1

    CS = states.H  # Инициализация состояния CS
    c = fd.read(1)  # Чтение первого символа из файла
    while c:
        if CS == states.H:  # Если текущее состояние H
            # Пропуск пробелов, табуляций и переходов на новую строку
            while c == ' ' or c == '\t' or c == '\n':
                c = fd.read(1)
            if ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or c == '_'):  # Если буква или _
                CS = states.ID  # Переход в состояние ID
            elif ((c >= '0' and c <= '9') or c == '.' or c == '+' or c == '-'):  # Если цифра или ., +, -
                CS = states.NM  # Переход в состояние NM
            elif c == ':':  # Если :
                CS = states.ASGN  # Переход в состояние ASGN
            else:
                CS = states.DLM  # Переход в состояние DLM

        elif CS == states.ASGN:  # Если текущее состояние ASGN
            colon = c
            c = fd.read(1)
            if c == '=':  # Если после : следует =
                # Создание токена оператора ":="
                tok = token(tok_names.OPER, ":=")
                add_token(tok)  # Добавление токена в таблицу лексем
                c = fd.read(1)
                CS = states.H
            else:
                err_symbol = colon
                CS = states.ERR  # Ошибка - неизвестный символ

        elif CS == states.DLM:  # Если текущее состояние DLM
            if c in ['(', ')', ';']:  # Если символ (, ), ;
                # Создание токена разделителя
                tok = token(tok_names.DELIM, c)
                add_token(tok)  # Добавление токена в таблицу лексем
                c = fd.read(1)
                CS = states.H
            elif c in ['<', '>', '=']:  # Если символ <, >, =
                # Создание токена оператора
                tok = token(tok_names.OPER, c)
                add_token(tok)  # Добавление токена в таблицу лексем
                c = fd.read(1)
                CS = states.H
            else:
                err_symbol = c
                c = fd.read(1)
                CS = states.ERR  # Ошибка - неизвестный символ

        elif CS == states.ERR:  # Если текущее состояние ERR
            print("\nUnknown character: {}\n".format(err_symbol))
            CS = states.H  # Возвращение в состояние H

        elif CS == states.ID:  # Если текущее состояние ID
            buf = []
            buf.append(c)
            c = fd.read(1)
            while (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9') or (c == '_'):
                buf.append(c)
                c = fd.read(1)
            buf = ''.join(buf)
            if is_kword(buf):  # Если идентификатор является ключевым словом
                # Создание токена ключевого слова
                tok = token(tok_names.KWORD, buf)
            else:
                # Создание токена идентификатора
                tok = token(tok_names.IDENT, buf)
            add_token(tok)  # Добавление токена в таблицу лексем
            CS = states.H  # Возвращение в состояние H

    fd.close()  # Закрытие файла

# Проверка, является ли идентификатор ключевым словом
def is_kword(id):
    return id in keywords

# Добавление токена в таблицу лексем
def add_token(tok):
    global lt, lt_head
    lex_entry = lexeme_table(tok)
    if lt is None:
        lt = lex_entry
        lt_head = lex_entry
    else:
        lt.next = lex_entry
        lt = lt.next

    print("Token created - name:", tok.token_name, "value:", tok.token_value)

# Вызов функции лексического анализа
filename = "C:\\Users\\artez\\Desktop\\example.txt"
lexer(filename)