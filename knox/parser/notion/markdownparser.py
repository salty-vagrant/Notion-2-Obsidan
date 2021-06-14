from ..base import IParser, IAST
from ply.yacc import yacc  # type: ignore
from ply.lex import lex  # type: ignore

from . import markdown_tokens as tokens
from . import markdown_rules as rules


class MarkdownParser(IParser):
    def __init__(self):
        self._lexer = lex(module=tokens)
        self._parser = yacc(module=rules)

    def parse(self, content: str) -> IAST:
        return self._parser.parse(content)
