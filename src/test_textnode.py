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
        self.assertEqual(node.text_type.value, "link")

    def test_url_value(self):
        node = TextNode("This is a url test", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
