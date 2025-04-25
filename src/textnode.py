from enum import Enum
from typing import Dict, Optional

from leafnode import LeafNode


class TextType(Enum):
    NORMAL = "TextType.NORMAL"
    BOLD = "TextType.BOLD"
    ITALIC = "TextType.ITALIC"
    CODE = "TextType.CODE"
    LINK = "TextType.LINK"
    IMAGE = "TextType.IMAGE"


class TextNode:
    # --- mapping table lives on the class ---------------------------------
    # text_type          tag     needs_url  self_closing
    _HTML_MAP: Dict[TextType, tuple[Optional[str], bool, bool]] = {
        TextType.NORMAL: (None, False, False),
        TextType.BOLD: ("b", False, False),
        TextType.ITALIC: ("i", False, False),
        TextType.CODE: ("code", False, False),
        TextType.LINK: ("a", True, False),
        TextType.IMAGE: ("img", True, True),
    }
    # ----------------------------------------------------------------------

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_leaf(self) -> LeafNode:
        """
        Convert *this* TextNode to a LeafNode suitable for an HTML tree.
        """
        try:
            tag, needs_url, self_closing = self._HTML_MAP[self.text_type]
        except KeyError as exc:
            raise ValueError(f"Unsupported TextType: {self.text_type}") from exc

        # Validate URL where required
        if needs_url:
            if not self.url:
                raise ValueError(f"{self.text_type.name} node requires a non-empty URL")
            attr_key = "src" if self_closing else "href"
            attrs = {attr_key: self.url}
            if self_closing:  # IMAGE: ensure alt attribute exists
                attrs.setdefault("alt", "")

        else:
            attrs = None

        return LeafNode(tag, None if self_closing else self.text, attrs)
