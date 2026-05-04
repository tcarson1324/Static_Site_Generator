from enum import Enum
import unittest

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING =  "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith("#"):
        hashes = 0
        while hashes < len(block) and block[hashes] == "#":
            hashes += 1
        if 1 <= hashes <= 6 and block[hashes] == " ":
            return BlockType.HEADING
        
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    elif block.startswith('>') and len(block) > 1:
        return BlockType.QUOTE
    
    lines = block.split("\n")
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    expected = 1
    is_ordered = True
    for line in lines:
        prefix = str(expected) + ". "
        if not line.startswith(prefix):
            is_ordered = False
            break
        expected += 1
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
class TestBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
    def test_heading_six(self):
        self.assertEqual(block_to_block_type("###### Title"), BlockType.HEADING)
    def test_code(self):
        self.assertEqual(block_to_block_type("```\nThis is some code\n```"), BlockType.CODE)
    def test_quote(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
    def test_unordered(self):
       block = "- one\n- two\n- 3"
       self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    def test_bad_unordered(self):
        block = "- one\n-two\n- 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_ordered(self):
       block = "1. one\n2. two\n3. 3"
       self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)