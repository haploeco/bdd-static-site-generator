import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_extra_newlines(self):
        md = """
    This is **bolded** paragraph




    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line


    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_longer_list(self):
        md = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_block_to_block_type_with_heading(self):
        md = """
# This is a heading
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.HEADING)

    def test_block_to_block_type_with_paragraph(self):
        md = """
This is a paragraph. There may be a lot of things here.
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_multiline_paragraph(self):
        md = """
This is a paragraph. There may be a lot of things here
and it may be on two lines.
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_code_block(self):
        md = """
```print("Hello World")```
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.CODE)

    def test_block_to_block_type_with_code_block_missing_close(self):
        md = """
```print("Hello World")
        """
        blocks = block_to_block_type(md.strip())
        self.assertNotEqual(blocks, BlockType.CODE)

    def test_block_to_block_type_with_quote(self):
        md = """
> This is a quote
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.QUOTE)

    def test_block_to_block_type_with_unordered_list(self):
        md = """
- This is a list
- with items
- This is another list item
- And yet another list item
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_with_ordered_list(self):
        md = """
1. This is a list
2. with items
3. This is another list item
4. And yet another list item
        """
        blocks = block_to_block_type(md.strip())
        self.assertEqual(blocks, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
