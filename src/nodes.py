from extraction import extract_markdown_images, extract_markdown_links
from leafnode import LeafNode
from textnode import TextNode, TextType

# Set DELIM_TO_STYLE table for use everywhere
DELIM_TO_STYLE = {
    "**": TextType.BOLD,
    "__": TextType.ITALIC,
    "`": TextType.CODE,
}


# Convert a TextNode to an HTMLNode (LeafNode)
def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode
    (specfically a LeafNode)
    """
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": ""})
    else:
        raise ValueError(f"Unknown text_type: {text_node.text_type}")


def split_nodes_delimiter(nodes, delimiter: str, default_style: TextType):
    """
    Split the text content of *nodes* on *delimiter* and return a list of
    TextNode instances whose `text_type` is toggled according to the delimiter.

    • If the delimiter is not present or default_style is NORMAL, the original
      nodes are returned unchanged.
    • Raises ValueError if a delimiter is opened but not closed.
    """

    if default_style is not TextType.NORMAL:
        return [nodes]  # nothing to transform

    # Map delimiters to the text style they introduce
    # delim_style = {
    #     "**": TextType.BOLD,
    #     "__": TextType.ITALIC,
    #     "`": TextType.CODE,
    # }.get(delimiter)
    alt_style = DELIM_TO_STYLE.get(delimiter)

    if alt_style is None:
        raise ValueError(f"Invalid delimiter: {delimiter!r}")  # not a valid delimiter

    parts = nodes.text.split(delimiter)
    if len(parts) % 2 == 0:  # odd → properly closed, even → unclosed
        raise ValueError(
            f"Invalid markdown syntax detected: no closing {delimiter!r} found"
        )

    result = [
        TextNode(segment, alt_style if i % 2 else TextType.NORMAL)
        for i, segment in enumerate(parts)
    ]

    return result


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
