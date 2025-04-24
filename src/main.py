from textnode import TextNode, TextType


def main():
    my_link_text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.cnn.com"
    )

    print(my_link_text_node)


if __name__ == "__main__":
    main()
