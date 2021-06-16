# module: markdown_rules.py
# PLY Parser rules for Notion markdown

from .markdown_tokens import tokens

precedence = (
    #    ("left", "PRIO0"),
    #    ("left", "PRIO1"),
    ("left", "PRIO2"),
)


def p_doc(p):
    """doc : empty
    | blocks"""


def p_blocks(p):
    """blocks : block
    | blocks block"""


def p_block(p):
    """block : content_block
    | blank_lines content_block"""


def p_content_block(p):
    """content_block : block_quote"""


# | verbatim
# | note
# | reference
# | horizontal_rule
# | heading
# | ordered_list
# | bullet_list
# | html_block
# | style_block
# | para
# | plain
# """


def p_blank_lines(p):
    """blank_lines : blank_line
    | blank_lines blank_line"""


def p_blank_line(p):
    """blank_line :  WHITESPACE NEWLINE
    | empty NEWLINE"""


def p_block_quote(p):
    """block_quote : block_quote_line
    | block_quote block_quote_line"""


def p_block_quote_line(p):
    "block_quote_line : NEWLINE RANGLE para %prec PRIO2"


def p_verbatim(p):
    pass


def p_note(p):
    pass


def p_reference(p):
    pass


def p_horizontal_rule(p):
    pass


def p_heading(p):
    pass


def p_ordered_list(p):
    pass


def p_bullet_list(p):
    pass


def p_style_block(p):
    pass


def p_html_block(p):
    pass


def p_para(p):
    "para : <Down>CONTENTS NEWLINE"


def p_plain(p):
    pass


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    print("Failed parsing input")
