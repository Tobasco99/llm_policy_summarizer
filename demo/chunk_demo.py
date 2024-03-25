import streamlit as st
from helper.splitter import load_and_split_text


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
    chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=0, max_value=10000, step=100, value=0)
    chunk_method = st.sidebar.selectbox("Chunking Method", ["XML","Text Structure"])
        
    uploaded_file = st.file_uploader('Choose your policy document (xml after GROBID)', type=['html','xml'])
            
    if uploaded_file != None:
        try:
            docs = load_and_split_text(uploaded_file, chunk_size, chunk_overlap, chunk_method)
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