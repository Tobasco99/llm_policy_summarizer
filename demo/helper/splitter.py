from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
import os
from dotenv import load_dotenv, find_dotenv
from tempfile import NamedTemporaryFile
import requests
from langchain_openai import OpenAIEmbeddings
from helper.xmlTagSplitter import XMLTagTextSplitter
from helper.sentence_splitter import XMLSentenceSplitter
from helper.weaviate_connection import WeaviateConnection

def __save_uploaded_file(uploaded_file:bytes):
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

def __delete_file(file_path:str):
    """
    Deletes the file from the server.

    Parameters
    ----------    
    file_path (str): The path of the file to be deleted.
    """
    os.remove(file_path)

def __get_html_splitter(chunk_size:int, chunk_overlap:int):
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

def __get_docs_from_structure_splitter(chunk_size:int, file_path:str):

    text_splitter = XMLTagTextSplitter(first_tag="div", second_tag="p", max_chunk_size=chunk_size)

    table_splitter = XMLTagTextSplitter(first_tag="figure", second_tag="row", max_chunk_size=chunk_size)

    docs = text_splitter.split_text_from_file(file_path)
    docs.append(table_splitter.split_text_from_file(file_path))

    return docs


def load_and_split_text(text:str, chunk_size:int, chunk_overlap:int, splitter_type:str):
    """Retrieve the file splitted in documents with given parameters.

    Parameters
    ----------
    text (BytesIO): The uploaded file object.
    chunk_size (int): size of the resulting chunks.
    chunk_overlap(int): the size of the chunk overlap.
    splitter_type (str): the desired way of splitting the text.

    Returns
    -------
    List[str]: a list of document chunks.
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

def vectorize_docs(docs:list, vectorizer:str, key:str, title:str = "dummy"):
    """Retrieve the file splitted in documents with given parameters.

    Parameters
    ----------
    docs (List[str]): The list of document chunks.
    vectorizer (str): The intended vectorizer to use.
    key(str): The OpenAI key.
    title(str): The document title.

    Returns
    -------
    List[number]: the vectorized chunks.
    """
    load_dotenv(find_dotenv())
    ol_url = os.environ.get("OLLAMA_URL")
    embed_url = ol_url+'/api/embeddings'
    embeddings = []

    if vectorizer == "OpenAI Embeddings":
        if key is None:
            raise ValueError
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small",api_key=key)
        embeddings = embedding_model.embed_documents(texts=docs[0:2])
        #embedding = embedding_model.embed_query(docs[0])

    elif vectorizer == "mxbai-embed-large":
        if ol_url is None:
            raise ValueError
        for doc in docs:
            body = {'model': 'mxbai-embed-large',
                    'prompt': doc}  
            response = requests.post(embed_url, json = body)
            embedding = response.json()["embedding"]
            embeddings.append(embedding)
        
    else:
        if ol_url is None:
            raise ValueError
        for doc in docs:
            body = {'model': 'nomic-embed-text',
                    'prompt': doc}  
            response = requests.post(embed_url, json = body)
            embedding = response.json()["embedding"]
            embeddings.append(embedding)

    # send embeddings to database
    weaviate = WeaviateConnection()
    weaviate.store_embeddings(embeddings=embeddings, chunks=docs[0:2], title=title)

    # later return none  
    return embeddings

