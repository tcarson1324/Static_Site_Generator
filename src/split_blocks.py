import unittest
def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)
    return result

class TestMarkToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_single_block(self):
        md = "Just one sentence"
        self.assertEqual(markdown_to_blocks(md), ["Just one sentence"])

    def test_extra_blank_lines(self):
        md = """

    First block



    Second block

    """

        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"]
        )
    def test_strip_whitespace(self):
        md = "   Block one   \n\n   Block two   "

        self.assertEqual(
            markdown_to_blocks(md),
            ["Block one", "Block two"]
        )

                
    def test_multiline_block(self):
        md = """Line one
    Line two
    Line three"""

        self.assertEqual(
            markdown_to_blocks(md),
            ["Line one\nLine two\nLine three"]
        )