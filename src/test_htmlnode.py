import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", None, None, {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.props_to_html()
        self.assertEqual(
            result,
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", None, None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", None, None, {})
        result = node.props_to_html()
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()