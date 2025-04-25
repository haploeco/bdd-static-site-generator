from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict = None,
    ):
        self.tag = tag
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children == []:
            raise ValueError("ParentNode must have children.")

        html = f"<{self.tag}{self.props_to_html()}>"

        # Loop through each child and add its HTML
        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html
