import re
import eurlex
from bs4 import BeautifulSoup as bs
from service.weaviate_connection import WeaviateConnection


def inject_knowledge(chunk):
    """
    Injects knowledge into the given chunk by replacing slash notation with knowledge tags.

    Args:
        chunk (str): The chunk of text to inject knowledge into.

    Returns:
        str: The modified chunk with knowledge tags.

    """
    matches = __extract_slash_notation(chunk)
    knowledge_dict = __create_knowledge_dict(matches)
    for slash_notation, content in knowledge_dict.items():
        chunk = chunk.replace(slash_notation, f"<ent>{slash_notation}</ent><ent_desc>{content}</ent_desc>")
    return chunk

def __extract_slash_notation(text):
    """
    Extracts slash notation (e.g., 12/2022) from the given text.

    Args:
        text (str): The text to search for slash notation.

    Returns:
        list: A list of slash notation found in the text.
    """
    pattern = r'\d{1,3}\/\d{4}'
    matches = re.findall(pattern, text)
    return matches

def __get_abstract(html):
    """
    Extracts the abstract from an HTML document.

    Args:
        html (str): The HTML document.

    Returns:
        str: The extracted abstract.

    Raises:
        Exception: If an error occurs during the extraction process.
    """

    try:
        soup = bs(html, features="html.parser")
        p_tags_text = []
        p_tags = soup.find_all("p")
        start = False
        end = False

        for p_tag in p_tags:
            if p_tag.text == "Article 1" or p_tag.text == "Article 1":
                start = True
            if p_tag.text == "Article 2" or p_tag.text == "Article 2":
                start = False
                end = True
            if start:
                p_tags_text.append(p_tag.text)
            if end:
                break

        abstract = ' '.join(p_tags_text[2:])
    except Exception as e:
        abstract = "A policy"
    
    return abstract


def __create_knowledge_dict(slash_notations):
    """
    Creates a dictionary of knowledge by retrieving content from EurLex API.

    Args:
        slash_notations (list): A list of slash notations.

    Returns:
        dict: A dictionary where the keys are slash notations and the values are the corresponding content.

    """
    knowledge_dict = {}
    weaviate = WeaviateConnection()
    for slash_notation in slash_notations:
        knowledge = weaviate.get_knowledge(slash_notation)
        if knowledge is not None:
            knowledge_dict[slash_notation] = knowledge
            continue
        celex = eurlex.get_celex_id(slash_notation=slash_notation)
        html = eurlex.get_html_by_celex_id(celex)
        content = __get_abstract(html)
        knowledge_dict[slash_notation] = content
        weaviate.store_knowledge(slash_notation, content)
    return knowledge_dict