from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.props = props if props is not None else {}
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        if self.tag == "a":
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
