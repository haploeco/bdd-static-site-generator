import unittest

from leafnode import LeafNode


class TestLeafeNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "http://haplolabs.io"})
        self.assertEqual(node.to_html(), '<a href="http://haplolabs.io">Click me!</a>')


if __name__ == "__main__":
    unittest.main()
