from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
import os
from tempfile import NamedTemporaryFile
import sys
sys.path.append('demo/helper')
from xmlTagSplitter import XMLTagTextSplitter
from langchain_text_splitters import HTMLHeaderTextSplitter


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

def __get_structure_splitter():
    tags_to_split_on = [
        ("div", "paragraph"),
        ("head", "header"),
        ("table", "table"),
    ]
    tag_splitter = XMLTagTextSplitter(tags_to_split_on=tags_to_split_on)
    return tag_splitter


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

    loader = UnstructuredXMLLoader(file_path)
    docs_raw = loader.load()
    
    if splitter_type == "XML":
        splitter = __get_html_splitter(chunk_size, chunk_overlap)
        with open(file_path, "r", encoding="utf-8") as file:
        # Read the content of the file
            content = file.read()
        docs = splitter.split_text(content)

    elif splitter_type == "Text Structure":
        splitter = __get_structure_splitter()
        docs = splitter.split_text_from_file(file_path)

    else:
        #todo
        splitter = __get_html_splitter(chunk_size, chunk_overlap)

    __delete_file(file_path)

    return docs

