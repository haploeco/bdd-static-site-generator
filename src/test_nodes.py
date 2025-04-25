import unittest

from nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)
from textnode import TextNode, TextType


class TestLeafNode(unittest.TestCase):
    def test_split_delimiter_bold(self):
        node = TextNode("This text has **bold text** in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(node, "**", TextType.NORMAL)
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("bold text", TextType.BOLD),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_italic(self):
        node = TextNode("This text has __italic text__ in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(node, "__", TextType.NORMAL)
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_code(self):
        node = TextNode("This text has `code text` in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(node, "`", TextType.NORMAL)
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("code text", TextType.CODE),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_not_found(self):
        node = TextNode("This text has no delimiter in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(node, "**", TextType.NORMAL)
        self.assertListEqual(
            [TextNode("This text has no delimiter in it", TextType.NORMAL)], new_nodes
        )

    def test_split_delimiter_no_closing_tag(self):
        node = TextNode("This text has **bold text in it", TextType.NORMAL)
        with self.assertRaises(ValueError) as raises_cm:
            split_nodes_delimiter(node, "**", TextType.NORMAL)

        exception = raises_cm.exception
        self.assertEqual(
            str(exception), "Invalid markdown syntax detected: no closing '**' found"
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [imgur](https://i.imgur.com) and another [best dev training](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("imgur", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("best dev training", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
