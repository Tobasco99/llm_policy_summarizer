from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
import os
from tempfile import NamedTemporaryFile

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
    
    if splitter_type == "html":
        splitter = __get_html_splitter(chunk_size, chunk_overlap)
    elif splitter_type == "semantic":
        #todo
        splitter = __get_html_splitter(chunk_size, chunk_overlap)
    else:
        #todo
        splitter = __get_html_splitter(chunk_size, chunk_overlap)
    
    docs_raw_text = [doc.page_content for doc in docs_raw]
    docs = splitter.create_documents(docs_raw_text)
    __delete_file(file_path)

    return docs

