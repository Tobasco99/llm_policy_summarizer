import streamlit as st
import requests
from helper.splitter import load_and_split_text
from FlagEmbedding import BGEM3FlagModel
from langchain_openai import OpenAIEmbeddings



def vectorize_docs(docs, vectorizer, key):
    url = 'http://137.226.232.15:11434/api/embeddings'


    #add functions for handling the vectorizer (helper)
    if vectorizer == "OpenAI Embeddings":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small",api_key=key)
        embedding = embeddings.embed_query(docs[0])


    elif vectorizer == "BGE-M3":
        #todo
        model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True)
        embedding = model.encode(docs[0], 
                            batch_size=12, 
                            max_length=2000, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
    else:
        body = {'model': 'nomic-embed-text',
                'prompt': docs[0]}  
        embedding = requests.post(url, json = body)
      
    return embedding

def main():
    st.set_page_config(layout="wide")

    st.title("Policy Chunking Demo")
    chunk_size = st.sidebar.slider("Chunk Size", min_value=100, max_value=10000, step=100, value=2000)
    chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=0, max_value=10000, step=100, value=0)
    chunk_method = st.sidebar.selectbox("Chunking Method", ["XML","Text Structure","Sentence"])
    openai_key = st.text_input('Enter OpenAI Key (only for OpenAI embeddings):')
    uploaded_file = st.file_uploader('Choose your policy document (xml received from GROBID)', type=['html','xml'])
            
    if uploaded_file != None:
        try:
            docs = load_and_split_text(uploaded_file, chunk_size, chunk_overlap, chunk_method)
            st.write(docs[0:5])
        except ValueError:
            st.warning("Chunk size needs to be larger than overlap!")

        vectorizer = st.selectbox("Vectorizer", ["OpenAI Embeddings", "BGE-M3", "nomic-embed-text-v1.5"])
                
        if st.button("Vectorize"):
            result = vectorize_docs(docs,vectorizer, openai_key)
            st.write("Vectors:")
            st.info(result[:5])


if __name__ == "__main__":
    main()