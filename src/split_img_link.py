from htmlnode import HTMLNode
from textnode import TextNode, TextType
from markdown_regex import extract_markdown_images, extract_markdown_links
import unittest

from split_delim import split_nodes_delimiter
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        for anchor, url in links:
            parts = text.split(f"[{anchor}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor, TextType.LINK, url ))
                text = parts[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            parts = text.split(f"![{alt}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode(
            "This is text ![cat](cat.jpg) end",
            TextType.TEXT
        )

        result = split_nodes_image([node])

        self.assertEqual(
            result,
            [
                TextNode("This is text ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.jpg"),
                TextNode(" end", TextType.TEXT),
            ]
        )

    def test_multiple_images(self):
        node = TextNode(
            "Start ![cat](cat.jpg) middle ![dog](dog.png) end",
            TextType.TEXT
        )

        result = split_nodes_image([node])

        self.assertEqual(
            result,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.jpg"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png"),
                TextNode(" end", TextType.TEXT),
            ]
        )

    def test_no_images(self):
        node = TextNode(
            "Just normal text",
            TextType.TEXT
        )

        result = split_nodes_image([node])

        self.assertEqual(
            result,
            [
                TextNode("Just normal text", TextType.TEXT)
            ]
        )

    def test_non_text_node(self):
        node = TextNode(
            "cat",
            TextType.IMAGE,
            "cat.jpg"
        )

        result = split_nodes_image([node])

        self.assertEqual(
            result,
            [
                TextNode("cat", TextType.IMAGE, "cat.jpg")
            ]
        )


class TestTextToTextnodes(unittest.TestCase):
    
    def test_plain_text(self):
        result = text_to_textnodes("Just plain text")
        self.assertEqual(
            result,
            [TextNode("Just plain text", TextType.TEXT)]
        )
    
    def test_bold_text(self):
        result = text_to_textnodes("This is **bold** text")
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )
    
    def test_italic_text(self):
        result = text_to_textnodes("This is _italic_ text")
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ]
        )
    
    def test_code_text(self):
        result = text_to_textnodes("This is `code` text")
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ]
        )
    
    def test_image(self):
        result = text_to_textnodes("This is an ![image](image.jpg)")
        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.jpg")
            ]
        )
    
    def test_link(self):
        result = text_to_textnodes("This is a [link](https://example.com)")
        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com")
            ]
        )
    
    def test_mixed_formatting(self):
        result = text_to_textnodes("**bold** and _italic_ and `code`")
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ]
        )
    
    def test_image_and_link(self):
        result = text_to_textnodes("![image](img.jpg) and [link](https://example.com)")
        self.assertEqual(
            result,
            [
                TextNode("image", TextType.IMAGE, "img.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com")
            ]
        )
    
    def test_complex_text(self):
        result = text_to_textnodes("Check **bold** and ![cat](cat.jpg) and [link](url.com) with _italic_ and `code`")
        self.assertGreater(len(result), 1)
        # Verify it contains expected node types
        types_found = {node.text_type for node in result}
        self.assertIn(TextType.TEXT, types_found)
        self.assertIn(TextType.BOLD, types_found)
        self.assertIn(TextType.IMAGE, types_found)
        self.assertIn(TextType.LINK, types_found)
        self.assertIn(TextType.ITALIC, types_found)
        self.assertIn(TextType.CODE, types_found)
        






