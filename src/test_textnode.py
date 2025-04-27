import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_link_type(self):
        node = TextNode("This is a link node", TextType.LINK, "www.haplolabs.io")
        self.assertEqual(node.text_type, TextType.LINK)

    def test_url_value(self):
        node = TextNode("This is a url test", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code block text node", TextType.CODE)
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block text node")

    def test_link(self):
        node = TextNode(
            "This is a link text node", TextType.LINK, "https://example.com"
        )
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode(None, TextType.IMAGE, "https://example.com")
        html_node = node.to_leaf()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt": ""})


if __name__ == "__main__":
    unittest.main()
