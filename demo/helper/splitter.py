from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
import os
from tempfile import NamedTemporaryFile
import sys
sys.path.append('demo/helper')
from xmlTagSplitter import XMLTagTextSplitter
from sentence_splitter import XMLSentenceSplitter



def __save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to a temporary location on the server.

    Parameters
    ----------

    uploaded_file (BytesIO): The uploaded file object.

    Returns
    -------
    str: The file path where the uploaded file is saved.
    """
    
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name
    return file_path

def __delete_file(file_path):
    """
    Deletes the file from the server.

    Parameters
    ----------    
    file_path (str): The path of the file to be deleted.
    """
    os.remove(file_path)

def __get_html_splitter(chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter

def __get_sentence_splitter():
    tags_to_split_on = [
        ("p", "sentence"),
        ("figdesc", "figure description"),
        ("row", "table row")
    ]
    tag_splitter = XMLSentenceSplitter(tags_to_split_on=tags_to_split_on)
    return tag_splitter

def __get_docs_from_structure_splitter(chunk_size, file_path):

    text_splitter = XMLTagTextSplitter(first_tag="div", second_tag="p", max_chunk_size=chunk_size)

    table_splitter = XMLTagTextSplitter(first_tag="figure", second_tag="row", max_chunk_size=chunk_size)

    docs = text_splitter.split_text_from_file(file_path)
    docs.append(table_splitter.split_text_from_file(file_path))

    return docs


def load_and_split_text(text, chunk_size, chunk_overlap, splitter_type):
    """Retrieve the file splitted in documents with given parameters.

    Parameters
    ----------
    text (BytesIO): The uploaded file object.
    chunk_size (int): size of the resulting chunks.
    chunk_overlap(int): the size of the chunk overlap.
    splitter_type (str): the desired way of splitting the text.

    Returns
    -------
    List[Document]: a list of document chunks.
    """

    file_path = __save_uploaded_file(text)
    
    if splitter_type == "XML":
        splitter = __get_html_splitter(chunk_size, chunk_overlap)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        docs = splitter.split_text(content)[2:]

    elif splitter_type == "Text Structure":
        docs = __get_docs_from_structure_splitter(chunk_size, file_path)

    else:
        splitter = __get_sentence_splitter()
        docs = splitter.split_text_from_file(file_path)

    __delete_file(file_path)

    return docs

