from textnode import TextNode, TextType, text_node_to_html
from blocktypes import BlockType, block_to_block_type
from split_blocks import markdown_to_blocks
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from split_img_link import split_nodes_link, split_nodes_image, text_to_textnodes 
import unittest
import os
import shutil
def text_to_children(text):
    text = " ".join(text.split())
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html(node))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            new_node = ParentNode("p", text_to_children(block))
        elif block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            text = block[level:].strip()
            new_node = ParentNode(f"h{level}", text_to_children(text))
        elif block_type == BlockType.CODE:
            code_text = block[3:-3].strip()
            code_text = "\n".join(line.strip() for line in code_text.splitlines())
            if code_text and not code_text.endswith("\n"):
                code_text += "\n"
            text_node = TextNode(code_text, TextType.CODE)
            html_node = text_node_to_html(text_node)
            new_node = ParentNode("pre", [html_node])
        elif block_type == BlockType.QUOTE:
            text = "\n".join(line[1:].strip() for line in block.split("\n"))
            new_node = ParentNode("blockquote", text_to_children(text))
                
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                text = line[2:]
                items.append(ParentNode("li", text_to_children(text)))
                new_node = ParentNode("ul", items)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                text = line[3:]
                items.append(ParentNode("li", text_to_children(text)))
                new_node = ParentNode("ol", items)
        children.append(new_node)
    return ParentNode("div", children)
def copy_recursive(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    items = os.listdir(src)
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_recursive(src_path, dst_path)
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")

class TestExtract(unittest.TestCase):
    def test_basic(self):
        markdown = "# Test"
        self.assertEqual("Test", extract_title(markdown))
    def test_two(self):
        markdown = "## Test"
        with self.assertRaises(Exception):
            extract_title(markdown)
    def test_no_space(self):
        markdown = "#Test"
        with self.assertRaises(Exception):
            extract_title(markdown)
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path) and full_path.endswith(".md"):
            
            rel_path = os.path.relpath(full_path,dir_path_content)
            dest_file = rel_path.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(full_path, template_path, dest_path)
        elif os.path.isdir(full_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(full_path, template_path, new_dest_dir)



def main():
    copy_recursive("static", "public")
    generate_pages_recursive("content", "src/template.html", "public")






if __name__ == "__main__":
    main()