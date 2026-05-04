from textnode import TextType, TextNode
import unittest
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes

class TestDelim(unittest.TestCase):
    def test_code_split(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_no_split(self):
        node = TextNode("hello world", TextType.TEXT)

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        expected = [
            TextNode("hello world", TextType.TEXT)
        ]

        self.assertEqual(result, expected)
    
    def test_bold_split(self):
        node = TextNode("This is **bold** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)
    def test_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)








