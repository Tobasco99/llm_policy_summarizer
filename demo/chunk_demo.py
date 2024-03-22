import streamlit as st
import os
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import GrobidParser


def save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to a temporary location on the server.

    Parameters
    ----------

    uploaded_file (BytesIO): The uploaded file object.

    Returns
    -------
    str: The file path where the uploaded file is saved.
    """
    
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name
    return file_path

def delete_file(file_path):
    """
    Deletes the file from the server.

    Parameters
    ----------    
    file_path (str): The path of the file to be deleted.
    """
    os.remove(file_path)


@st.cache_data
def setup_documents(uploaded_file, chunk_size, chunk_overlap, chunk_method):
    """Retrieve the file splitted in documents with given parameters.

    Parameters
    ----------
    uploaded_file (BytesIO): The uploaded file object.
    chunk_size (int): size of the resulting chunks.
    chunk_overlap(int): the size of the chunk overlap.
    chunk_method (str): the desired way of splitting the text.

    Returns
    -------
    List[Document]: a list of document chunks.
    """

    file_path = save_uploaded_file(uploaded_file)

    #Produce chunks from article paragraphs
    loader = GenericLoader.from_filesystem(
    file_path,
    parser= GrobidParser(segment_sentences=False)
    )
    docs_raw = loader.load()

    # switch loader and splitter
    #loader = PyPDFLoader(file_path)
    #docs_raw = loader.load()

    docs_raw_text = [doc.page_content for doc in docs_raw]


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap)
    docs = text_splitter.create_documents(docs_raw_text)
    # Delete the file after use
    #delete_file(file_path)
    return docs

def vectorize_docs(docs, vectorizer):
    #add functions for handling the vectorizer (helper)
    if vectorizer == "OpenAI Embeddings":
        pass
    elif vectorizer == "BGE-M3":
        pass
    else:
        pass

def main():
    st.set_page_config(layout="wide")

    st.title("Policy Chunking Demo")
    chunk_size = st.sidebar.slider("Chunk Size", min_value=100, max_value=10000, step=100, value=2000)
    chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=100, max_value=10000, step=100, value=200)
    chunk_method = st.sidebar.selectbox("Chunking Method", ["Recursive Character","Semantic" ,"HTML/XML Tag"])
        
    uploaded_file = st.file_uploader('Choose your policy document', type='pdf')
            
    if uploaded_file != None:
        try:
            docs = setup_documents(uploaded_file, chunk_size, chunk_overlap, chunk_method)
            st.write(docs[0:5])
        except ValueError:
            st.warning("Chunk size needs to be larger than overlap!")

        vectorizer = st.selectbox("Vectorizer", ["OpenAI Embeddings", "BGE-M3", "nomic-embed-text-v1.5"])
                
        if st.button("Vectorize"):
            result = vectorize_docs(docs,vectorizer)
            st.write("Vectors:")
            st.info(result)


if __name__ == "__main__":
    main()