from ..base import IParser, IAST


class MarkdownParser(IParser):
    def parse(self, content: str) -> IAST:
        pass
