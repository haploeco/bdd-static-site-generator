from enum import Enum


class BlockType(Enum):
    """
    Enum for block types.
    """

    PARAGRAPH = "BlockType.PARAGRAPH"
    HEADING = "BlockType.HEADING"
    CODE = "BlockType.CODE"
    QUOTE = "BlockType.QUOTE"
    UNORDERED_LIST = "BlockType.UNORDERED_LIST"
    ORDERED_LIST = "BlockType.ORDERED_LIST"


def markdown_to_blocks(markdown: str) -> list:
    """
    Convert a string to a list of blocks.
    The separator is \n\n.
    """
    # Split the text into blocks
    blocks = markdown.split("\n\n")
    update_blocks = []

    # Loop through each block and assign to a list of strings
    for block in blocks:
        normalized_block = "\n".join(
            line.lstrip() for line in block.splitlines()
        ).strip()
        update_blocks.append(normalized_block)
        # If the block is empty, remove it from the list
        if not normalized_block:
            update_blocks.pop()

    # Convert each block to a list of TextNode instances
    # blocks = [text_to_textnodes(block) for block in blocks]

    return update_blocks


def block_to_block_type(md: str):
    """
    Convert a block to a block type.
    """
    # Check if the block is empty
    if not md:
        return BlockType.PARAGRAPH

    # Check if the block is a heading
    if md.startswith("#"):
        return BlockType.HEADING

    # Check if the block is a code block
    if md.startswith("```") and md.endswith("```"):
        return BlockType.CODE

    # Check if the block is a quote
    if md.startswith(">"):
        return BlockType.QUOTE

    # Check if the block is an unordered list
    if md.startswith("-") or md.startswith("*") or md.startswith("+"):
        return BlockType.UNORDERED_LIST

    # Check if the block is an ordered list
    if md[0].isdigit() and md[1] == ".":
        return BlockType.ORDERED_LIST

    # If none of the above, return paragraph
    return BlockType.PARAGRAPH
