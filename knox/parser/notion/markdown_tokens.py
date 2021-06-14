# module: markdown_tokens.py
# lexing rules for notion markdown

tokens = (
    "SEPARATOR",
    "LISTNUMBER",
    "LISTSINGLE",
    "LISTDOUBLE",
    "TAB",
    "SPACE",
    "WHITESPACE",
    "POUNDSIGN",
    "EXCLAMATION",
    "DOLLAR",
    "CODEFIELD",
    "NEWLINE",
    "CODE",
    "BOLD",
    "LATICS",
    "LANGLE",
    "RANGLE",
    "LBRACKET",
    "RBRACKET",
    "LPAREN",
    "RPAREN",
    "CONTENTS",
    "NEWLINE",
)


# Regular expression rules for simple tokens
def t_SEPARATOR(t):
    r"[\n\r]\s?[*\-=](\s?[*\-=]){2,}\s+"
    return t


def t_LISTNUMBER(t):
    r"[\n\r][\s\t]*[0-9]+\.\s"
    t.value = (t.value)[1:-2]
    return t


def t_LISTSINGLE(t):
    r"[\n\r][\s\t]*[\*\-\+]\s"
    t.value = (t.value)[1:-1]
    return t


def t_LISTDOUBLE(t):
    r"[\n\r][\s\t]*[\*\-\+]{2}\s"
    t.value = (t.value)[1:-2]
    return t


def t_TAB(t):
    r"\t"
    return t


def t_SPACE(t):
    r"\s+"
    return t


def t_WHITESPACE(t):
    r"[\t\s]+"
    return t


def t_POUNDSIGN(t):
    r"\s?[#]{1,6}"
    t.value = str(len(t.value))
    return t


def t_EXCLAMATION(t):
    r"\s?\!"
    return t


def t_DOLLAR(t):
    r"\$"
    return t


def t_CODEFIELD(t):
    r"[\n\r]\s?`{3}\s?"
    return t


def t_NEWLINE(t):
    r"[\r\n]"
    t.value = len(t.value)
    return t


def t_CODE(t):
    r"`"
    return t


def t_BOLD(t):
    r"[*_]{2}"
    return t


def t_LATICS(t):
    r"[*_]"
    return t


def t_LANGLE(t):
    r"<"
    return t


def t_RANGLE(t):
    r">"
    return t


def t_LBRACKET(t):
    r"\["
    return t


def t_RBRACKET(t):
    r"\]"
    return t


def t_LPAREN(t):
    r"[(]"
    return t


def t_RPAREN(t):
    r"[)]"
    return t


def t_CONTENTS(t):
    r'([0-9a-zA-Z]|[., :;/\'’?{}"\\+^#|=%&])+'
    return t


## Ignored only \n not \n\n
# def t_COMMENTS(t):
#    r'[\n\r]'
#    pass


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


# A string containing ignored characters (spaces and tabs)
# t_ignore  = '\n\t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
