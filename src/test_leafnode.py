from leafnode import LeafNode
import unittest
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com">Click</a>'
        )

    def test_leaf_multiple_props(self):
        node = LeafNode("a", "Click", {
            "href": "https://google.com",
            "target": "_blank"
        })
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com" target="_blank">Click</a>'
        )
        
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

