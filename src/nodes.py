from typing import Iterable, List

from extraction import extract_markdown_images, extract_markdown_links
from leafnode import LeafNode
from textnode import TextNode, TextType

# Set DELIM_TO_STYLE table for use everywhere
DELIM_TO_STYLE = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def split_nodes_delimiter(nodes: Iterable[TextNode], delimiter: str) -> List[TextNode]:
    """
    Walk over *nodes*.  For each node whose text_type is NORMAL and whose text
    contains *delimiter*, split its .text on that delimiter and toggle the
    style.  All other nodes are copied unchanged.

    Returns a brand-new list; the input list and its nodes are never mutated.

    Raises
    ------
    ValueError
        • Unknown delimiter
        • Unclosed delimiter sequence (odd number of delimiters)
    """
    alt_style = DELIM_TO_STYLE.get(delimiter)
    if alt_style is None:
        raise ValueError(f"Invalid delimiter: {delimiter!r}")

    out: List[TextNode] = []

    for node in nodes:
        # 1. Leave non-NORMAL nodes untouched
        if node.text_type is not TextType.NORMAL:
            out.append(node)
            continue

        # 2. No delimiter present → nothing to split
        if delimiter not in node.text:
            out.append(node)
            continue

        # 3. Split and rebuild
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:  # even ⇒ an opening delimiter was never closed
            raise ValueError(
                f"Invalid markdown syntax: no closing {delimiter!r} in {node.text!r}"
            )

        for idx, segment in enumerate(parts):
            style = alt_style if idx % 2 else TextType.NORMAL
            out.append(TextNode(segment, style))

    return out


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    """Split each TextNode around Markdown images and turn the images into
    `TextType.IMAGE` nodes.  Nodes without images are returned unchanged."""
    new_nodes: list[TextNode] = []

    for node in nodes:
        matches = extract_markdown_images(node.text)  # → list[(alt, url)]
        if not matches:  # fast-path: nothing to split
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in matches:
            before, _, after = remaining_text.partition(f"![{alt}]({url})")
            new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = after  # keep scanning the tail

        if remaining_text:  # whatever is left after last image
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    """Split each TextNode around Markdown links and turn the images into
    `TextType.LINK` nodes.  Nodes without links are returned unchanged."""
    new_nodes: list[TextNode] = []

    for node in nodes:
        matches = extract_markdown_links(node.text)  # → list[(alt, url)]
        if not matches:  # fast-path: nothing to split
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in matches:
            before, _, after = remaining_text.partition(f"[{alt}]({url})")
            new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining_text = after  # keep scanning the tail

        if remaining_text:  # whatever is left after last image
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Convert a string to a list of TextNode instances.
    """

    # Split the text into nodes
    nodes = [TextNode(text, TextType.NORMAL)]

    # Split the nodes on the delimiters
    for delim in DELIM_TO_STYLE.keys():
        nodes = split_nodes_delimiter(nodes, delim)

    # Split the nodes on images
    nodes = split_nodes_image(nodes)

    # Split the nodes on links
    nodes = split_nodes_link(nodes)

    return nodes
