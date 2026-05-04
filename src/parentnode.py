from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No child nodes")
        else:
            result = ""
            for child in self.children:
                result += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"     
