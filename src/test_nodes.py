import unittest

from nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestLeafNode(unittest.TestCase):
    def test_split_delimiter_bold(self):
        node = [TextNode("This text has **bold text** in it", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(node, "**")
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("bold text", TextType.BOLD),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_italic(self):
        node = [TextNode("This text has _italic text_ in it", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(node, "_")
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_code(self):
        node = [TextNode("This text has `code text` in it", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(node, "`")
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.NORMAL),
                TextNode("code text", TextType.CODE),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_delimiter_not_found(self):
        node = [TextNode("This text has no delimiter in it", TextType.NORMAL)]
        new_nodes = split_nodes_delimiter(node, "**")
        self.assertListEqual(
            [TextNode("This text has no delimiter in it", TextType.NORMAL)], new_nodes
        )

    def test_split_delimiter_no_closing_tag(self):
        node = [TextNode("This text has **bold text in it", TextType.NORMAL)]
        with self.assertRaises(ValueError) as raises_cm:
            split_nodes_delimiter(node, "**")

        exception = raises_cm.exception
        self.assertEqual(
            str(exception),
            "Invalid markdown syntax: no closing '**' in 'This text has **bold text in it'",
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

    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_more_links(self):
        node = TextNode(
            "This is [haplo](https://haplolabs.io) **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("haplo", TextType.LINK, "https://haplolabs.io"),
                TextNode(" ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
