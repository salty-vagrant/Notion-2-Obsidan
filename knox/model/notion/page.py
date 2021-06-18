from typing import List
from pathlib import Path
from markdown_it import MarkdownIt
from ..base import IPage, IDataStore, Link


class Page(IPage):
    def __init__(self):
        self._datastore = None
        self._path = None
        self._tokens = []

    @classmethod
    def from_datastore(cls, datastore: IDataStore, path: Path) -> "Page":
        if not datastore.exists(path):
            raise FileNotFoundError(f"Could not load {path} from {datastore.name}")
        new_page = cls()
        new_page.attach(datastore, path)
        return new_page

    @property
    def _parsed_page(self):
        if not self._tokens:
            self._tokens = MarkdownIt(self._content)
        return self._tokens

    def attach(self, datastore: IDataStore, path: Path):
        if not datastore.exists(path):
            raise FileNotFoundError(
                f"Could not attach Page to  {path} in {datastore.name}"
            )
        self._datastore = datastore
        self._path = path

    @property
    def on_page_links(self) -> List[Link]:
        # Walk all Tokens
        # if token.type == "link_open" or "img" then extact all the info into a Link and add to the list
        # if img mark as embedded link
        # get link text (if link) from next node (may require some rendering)
        # if link's href has a protocol
        #     if link is notion.so
        #         extract page name from url
        #         if extracted name == link text then set alt title = "" else set alt title = link text
        #         link text = extract page name
        #            [[link text|alt-name]] ^[original URL]
        # else (it is a structural link)
        #   process link to map to Obsidian format (basically convert escape "%.." and remove UID) this becomes map
        ...
