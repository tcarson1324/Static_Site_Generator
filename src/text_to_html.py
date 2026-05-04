from textnode import TextNode, TextType, text_node_to_html
import unittest

class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is a text node", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a text node")

    def test_italic(self):
        node = TextNode("another", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "another")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")


    def test_link(self):
        node = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "OpenAI")
        self.assertEqual(html_node.props, {"href": "https://openai.com"})


    def test_image(self):
        node = TextNode("logo", TextType.IMAGE, "https://site.com/logo.png")
        html_node = text_node_to_html(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://site.com/logo.png",
                "alt": "logo"
            }
        )
