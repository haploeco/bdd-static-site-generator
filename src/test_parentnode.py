import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("i", "grandchild2")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><i>grandchild2</i></span></div>",
        )

    def test_to_html_many_leaf_nodes(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
