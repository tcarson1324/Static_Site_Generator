import re
import unittest


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    Returns a list of tuples containing (alt_text, url) for each image.
    
    Markdown image syntax: ![alt text](url)
    """
    pattern = r"!\[([^\]]*)\]\(([^)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """
    Extract markdown links from text.
    Returns a list of tuples containing (anchor_text, url) for each link.
    
    Markdown link syntax: [anchor text](url)
    """
    pattern = r"\[([^\]]*)\]\(([^)]*)\)"
    matches = []
    for match in re.finditer(pattern, text):
        # Skip if preceded by !  (which would make it an image)
        if match.start() > 0 and text[match.start() - 1] == '!':
            continue
        matches.append((match.group(1), match.group(2)))
    return matches


class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            matches
        )
    
    def test_no_images(self):
        text = "This text has no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)
    
    def test_alt_text_with_spaces(self):
        matches = extract_markdown_images("![alt text with spaces](https://example.com/img.png)")
        self.assertListEqual([("alt text with spaces", "https://example.com/img.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )
    
    def test_no_links(self):
        text = "This text has no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_empty_anchor_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)
    
    def test_relative_urls(self):
        text = "[Home](/) and [About](/about) and [Contact](/contact)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("Home", "/"), ("About", "/about"), ("Contact", "/contact")],
            matches
        )
    
    def test_mixed_with_images(self):
        text = "Check out [this site](https://example.com) and ![image](https://example.com/img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this site", "https://example.com")], matches)
