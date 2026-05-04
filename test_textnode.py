import unittest
from textnode import TextNode, TextType  # or wherever yours are

class TestTextNode(unittest.TestCase):
    

    def test_eq(self):
        node1 = TextNode("hello", TextType.TEXT, None)
        node2 = TextNode("hello", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_different_text(self):
        node1 = TextNode("hello", TextType.TEXT, None)
        node2 = TextNode("bye", TextType.TEXT, None)
        self.assertNotEqual(node1, node2)

    def test_different_type(self):
        node1 = TextNode("hello", TextType.TEXT, None)
        node2 = TextNode("hello", TextType.BOLD, None)
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        node1 = TextNode("hello", TextType.LINK, "https://a.com")
        node2 = TextNode("hello", TextType.LINK, "https://b.com")
        self.assertNotEqual(node1, node2)

    def test_url_none_vs_value(self):
        node1 = TextNode("hello", TextType.TEXT, None)
        node2 = TextNode("hello", TextType.TEXT, "https://a.com")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()