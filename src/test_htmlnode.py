import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "p",
            "This is a what is in the paragraph",
            None,
            {"href": "www.haplolabs.io", "target": "_blank"},
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [])

    def test_props(self):
        node = HTMLNode(
            "p",
            "This is a what is in the paragraph",
            None,
            {"href": "www.haplolabs.io", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="www.haplolabs.io" target="_blank"'
        )

    def test_to_html(self):
        node = HTMLNode(
            "p",
            "This is a what is in the paragraph",
            None,
            {"href": "www.haplolabs.io", "target": "_blank"},
        )
        self.assertRaises(NotImplementedError, node.to_html)


if __name__ == "__main__":
    unittest.main()
