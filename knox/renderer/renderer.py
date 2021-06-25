from typing import List
import inspect
from abc import ABC, abstractmethod
from typing import Sequence
from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode


class RenderContext:
    indent_stack: List[str] = []


class Renderer(ABC):
    def __init__(self):
        self.rules = {
            k: v
            for k, v in inspect.getmembers(self, predicate=inspect.ismethod)
            if not (k.startswith("render") or k.startswith("_"))
        }
        self._current_nesting_level = 0

    def render(self, tokens: Sequence[Token]):
        root: SyntaxTreeNode = SyntaxTreeNode(tokens)
        ctx: RenderContext = RenderContext()
        result: str = self.renderNode(root, ctx)

        return result

    @abstractmethod
    def renderNode(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        ...
