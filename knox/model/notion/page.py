import re
from typing import List
from pathlib import Path
from urllib.parse import unquote, urlsplit
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins import dollarmath
from ..base import IPage, IDataStore, Link, BadPage
from knox.renderer.markdown import MarkdownRenderer
from knox.renderer import Renderer


UID_PATTERN = re.compile(r"\s[a-fA-f0-9]{32}$")


class Page(IPage):
    def __init__(self):
        self._datastore = None
        self._path = None
        self._tokens = []

    @classmethod
    def from_datastore(cls, datastore: IDataStore, path: Path) -> "Page":
        if not datastore.exists(path):
            raise BadPage(f"Could not load {path} from {datastore.name}")
        new_page = cls()
        new_page.attach(datastore, path)
        return new_page

    @classmethod
    def create_renderer(cls, ext: str, config: dict = {}) -> Renderer:
        if ext != r".md":
            raise NotImplementedError
        return MarkdownRenderer(config=config)

    @property
    def _parsed_page(self) -> List[Token]:
        if self._path.suffix != r".md":
            raise NotImplementedError(
                f"Cannot yet parse files of type {self._path.suffix}"
            )
        if not self._tokens:
            md = MarkdownIt("gfm-like").use(dollarmath.dollarmath_plugin)
            self._tokens = md.parse(self._content)
        return self._tokens

    @property
    def _content(self) -> str:
        return self._datastore.read_resource(self._path).decode()

    def attach(self, datastore: IDataStore, path: Path):
        if not datastore.exists(path):
            raise FileNotFoundError(
                f"Could not attach Page to  {path} in {datastore.name}"
            )
        self._datastore = datastore
        self._path = path

    def _extract_links_from_tokens(self, tokens: List[Token]) -> List[Link]:
        links = []
        for i, token in enumerate(tokens):
            link_text = ""
            if token.type == "inline":
                assert token.children is not None  # nosec
                links.extend(self._extract_links_from_tokens(token.children))
            elif token.type == "link_open" or token.type == "image":
                if token.type == "link_open":
                    href = str(token.attrs["href"])
                    link_text = tokens[i + 1].content
                else:
                    href = str(token.attrs["src"])
                    link_text = href
                    if Path(urlsplit(href).path).suffix == r".md":
                        link_name = unquote(Path(urlsplit(href).path).name)
                        link_text = UID_PATTERN.sub(r"", link_name)
                if urlsplit(href).netloc.startswith("notion.so") and not link_text:
                    link_name = Path(urlsplit(href).path).name
                    link_text = UID_PATTERN.sub(r"", link_name)
                links.append(
                    Link(name=link_text, uri=href, embedded=(token.type == "image"))
                )
        return links

    @property
    def on_page_links(self) -> List[Link]:
        links = self._extract_links_from_tokens(self._parsed_page)
        return links
