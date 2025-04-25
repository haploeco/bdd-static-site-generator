import re


def extract_markdown_images(markdown_text):
    """
    Extracts image URLs from markdown text.

    Args:
        markdown_text (str): The markdown text to extract images from.

    Returns:
        list: A list of image URLs.
    """
    # Regular expression to match markdown image syntax
    pattern = r"!\[(.*?)\]\((.*?)\)"
    # pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, markdown_text)
    return matches


def extract_markdown_links(markdown_text):
    """
    Extracts links from markdown text.

    Args:
        markdown_text (str): The markdown text to extract links from.

    Returns:
        list: A list of links.
    """
    # Regular expression to match markdown link syntax
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, markdown_text)
    return matches
