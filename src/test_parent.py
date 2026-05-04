from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import unittest


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
    def test_nested_children(self):
        node = ParentNode("div", [
            ParentNode("span", [
                LeafNode("b", "grandchild")
            ])
        ])
        self.assertEqual(node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_deep_nesting(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "deep")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>deep</p></article></section></div>"
        )
    def test_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_children_empty(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()