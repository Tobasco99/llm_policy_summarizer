import streamlit as st
from helper.splitter import load_and_split_text,vectorize_docs

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

        vectorizer = st.selectbox("Vectorizer", ["OpenAI Embeddings", "mxbai-embed-large", "nomic-embed-text-v1.5"])
                
        if st.button("Vectorize"):
            try:
                result = vectorize_docs(docs,vectorizer, openai_key)
            except ValueError:
                st.warning("OpenAI key is required!")
            st.write("Vectors:")
            st.info(result[:5])


if __name__ == "__main__":
    main()