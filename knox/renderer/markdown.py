from typing import List
import re
import textwrap
from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode
from .renderer import Renderer, RenderContext


# This is a kludge to deal with the odd way markup is used in these nodes
MARKUP_EXCEPTIONS: List[str] = ["bullet_list", "ordered_list", "block_quote"]

MULTI_NEWLINE = re.compile(r"\n+\Z")

# pylint: disable=no-self-use, unused-argument
class MarkdownRenderer(Renderer):
    def _render_children(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result = ""
        for _child in node.children:
            result += self.renderNode(_child, ctx)
        return result

    def renderNode(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = ""

        if node.type in self.rules:
            result = self.rules[node.type](node, ctx)
        else:
            result = self._render_children(node, ctx)
        if not node.is_root:
            _prefix: str = (
                "".join(ctx.indent_stack)
                if node.block and node.previous_sibling
                else ""
            )
            _suffix: str = ""
            if node.is_nested and node.markup and not node.type in MARKUP_EXCEPTIONS:
                if node.parent and node.parent.type == "ordered_list":
                    _prefix += str(ctx.list_counter[-1])
                _prefix += node.markup
                if node.block:
                    _prefix += " "
                if not node.block:
                    _suffix = f"{node.markup}"
            result = MULTI_NEWLINE.sub("\n", result)
            if node.block and not node.hidden:
                if node.next_sibling and result and result[-1] == "\n":
                    _suffix += ("".join(ctx.indent_stack)).rstrip()
                _suffix += "\n"
            result = _prefix + result + _suffix
        else:
            if result[-1] == "\n":
                result = result[:-1]
        return result

    def text(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        _prefix: str = ""
        if node.previous_sibling:
            _prefix = "".join(ctx.indent_stack)
        return _prefix + node.content

    def hr(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        return self._config["hr"] + "\n"

    def softbreak(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        return "\n"

    def fence(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = f"{node.markup}{node.info}\n{node.content}{node.markup}\n"
        return result

    def code_block(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = "\n    ".join(node.content.rstrip("\n").split("\n"))
        return "    " + result + "\n"

    def code_inline(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = f"{node.markup}{node.content}{node.markup}"

        if node.markup == "``":
            result = f"{node.markup} {node.content} {node.markup}"
        return result

    def math_inline(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = f"{node.markup}{node.content}{node.markup}"
        return result

    def math_block(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = f"{node.markup}{node.content}{node.markup}"
        return result + "\n"

    def heading(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = self._render_children(node, ctx)
        return result

    def image(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result = (
            f"![{self._render_children(node, RenderContext())}]({node.attrs['src']})"
        )
        return result

    def link(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result = (
            f"[{self._render_children(node, RenderContext())}]({node.attrs['href']})"
        )
        return result

    def blockquote(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        ctx.indent_stack.append("> ")
        result: str = self._render_children(node, ctx)
        ctx.indent_stack.pop()
        return result

    def ordered_list(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        ctx.list_counter.append(
            0 if self._config["ordered_list"]["count"] == "+" else 1
        )
        result = self._render_children(node, ctx)
        ctx.list_counter.pop()
        return result

    def list_item(self, node: SyntaxTreeNode, ctx: RenderContext) -> str:
        result: str = ""
        if node.parent is None:
            return result
        _indent_change: int = self._config[node.parent.type]["indent"]
        if self._config[node.parent.type]["count"] == "+":
            ctx.list_counter[-1] += 1
        ctx.indent_stack.append(" " * _indent_change)
        result += self._render_children(node, ctx)
        ctx.indent_stack.pop()
        result = result.rstrip("\n")
        return result
