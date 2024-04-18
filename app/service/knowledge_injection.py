import re
import eurlex

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
        chunk = chunk.replace(slash_notation, f"<knowledge>{content}</knowledge>")
    return chunk

def __extract_slash_notation(text):
    """
    Extracts slash notation dates (e.g., 12/2022) from the given text.

    Args:
        text (str): The text to search for slash notation dates.

    Returns:
        list: A list of slash notation dates found in the text.
    """
    pattern = r'\d{1,2}/\d{4}'
    matches = re.findall(pattern, text)
    return matches

def __get_abstract(html):
    #todo send to llm to get abstract summary
    return "abstract"


def __create_knowledge_dict(slash_notations):
    """
    Creates a dictionary of knowledge by retrieving content from EurLex API.

    Args:
        slash_notations (list): A list of slash notations.

    Returns:
        dict: A dictionary where the keys are slash notations and the values are the corresponding content.

    """
    knowledge_dict = {}
    for slash_notation in slash_notations:
        celex = eurlex.get_celex_id(slash_notation=slash_notation)
        html = eurlex.get_html_by_celex_id(celex)
        content = __get_abstract(html)
        knowledge_dict[slash_notation] = content
    return knowledge_dict