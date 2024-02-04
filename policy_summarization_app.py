import streamlit as st
import openai
import os
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]

map_template = """The following is a set of documents from a political policy:

{text}

Based on this list of documents, please summarize the key topics and decisions that were made.
SUMMARY:"""

combine_template = """The following is a set of summaries from a political policy:

{text}

Take these and distill it into a comprehensive summary for a person {knowledge} domain knowledge of the 
main topic. If present especially focus on the following topic: {focus}
If no topic is provided, just write a comprehensive summary including all topics.
SUMMARY:"""

refine_template = """Write a comprehensive summary of this video transcript. 

Divide it into,
1. Dopamine and Procrastination
2. Tools proposed
3. Protocols
4. Conclusion

{text}

SUMMARY:"""

def save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to a temporary location on the server.

    Args:
    uploaded_file (BytesIO): The uploaded file object.

    Returns:
    str: The file path where the uploaded file is saved.
    """
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name
    return file_path

def delete_file(file_path):
    """
    Deletes the file from the server.

    Args:
    file_path (str): The path of the file to be deleted.
    """
    os.remove(file_path)

def custom_summary(docs,llm, user_input, chain_type, domain_knowledge, temperature):
    COMBINE_PROMPT = PromptTemplate(template=combine_template, input_variables=["text"],
                                                partial_variables={"focus": user_input ,"knowledge": "with" if domain_knowledge else "without"})
    MAP_PROMPT = PromptTemplate(template=map_template, input_variables=["text"])
    if chain_type == "map_reduce":
        chain = load_summarize_chain(llm,chain_type=chain_type,
                                     map_prompt=MAP_PROMPT,
                                     combine_prompt=COMBINE_PROMPT,
                                     temperature=temperature)
    else:
        chain = load_summarize_chain(llm,chain_type=chain_type)
    
    summary_output = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]
    
    return summary_output

@st.cache_data
def setup_documents(uploaded_file, chunk_size, chunk_overlap):
    file_path = save_uploaded_file(uploaded_file)
    loader = PyPDFLoader(file_path)
    docs_raw = loader.load()
    docs_raw_text = [doc.page_content for doc in docs_raw]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap)
    docs = text_splitter.create_documents(docs_raw_text)
    # Delete the file after use
    delete_file(file_path)
    return docs

def main():
    st.set_page_config(layout="wide")
    tab1, tab2= st.tabs(["Summarization", "Ask your Policy"])
    q_a_visible = False

    with tab1:
        st.title("Policy Summarization App")
        chain_type = st.sidebar.selectbox("Chain Type", ["map_reduce", "refine"])
        chunk_size = st.sidebar.slider("Chunk Size", min_value=100, max_value=10000, step=100, value=2000)
        chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=100, max_value=10000, step=100, value=200)
        
        if st.sidebar.checkbox("Change prompt"):
            st.header("Enter your custom Prompt:")

            map_input = st.text_area("Map Prompt", "This is a test text for a possible prompt.")
            reduce_input = st.text_area("Reduce Prompt", "This is a test text for a possible prompt.")
            refine_input = st.text_area("Refine Prompt", "This is a test text for a possible prompt.")
        
        else:
            uploaded_file = st.file_uploader('Choose your policy document')
            user_prompt = st.text_input("Enter custom summarization requests")
            if uploaded_file is not None:
                df = "file"
            knowledge = st.toggle('Domain knowledge?')

            temperature = st.sidebar.number_input("LLM Temperature", min_value=0.0, max_value=1.0, step=0.1, value=0.0)
            
            # make the choice of llm to select from a selectbox
            llm = st.sidebar.selectbox("LLM", ["GPT3.5", "GPT4", ""])
            if llm == "ChatGPT":
                llm = "gpt3.5"
            elif llm == "GPT4":
                llm = "gpt4"
            
            if uploaded_file != None:
                q_a_visible = True
                docs = setup_documents(uploaded_file, chunk_size, chunk_overlap)
                st.write("Policy was loaded successfully")
                
                if st.button("Summarize"):
                    result = custom_summary(docs,llm, user_prompt, chain_type, knowledge, temperature)
                    st.write("Summary:")
                    st.info(result)
                    if st.button("Download"):
                        pass
                    refine_request = st.text_area("Adjust Summary", "This is a text area to enter possible feedback for a new summary.")
                    if st.button("Re-generate"):
                        pass
    with tab2:
        st.header("Ask your Policy")
        if q_a_visible:
            # Form input and query
            result = []
            with st.form('myform', clear_on_submit=True):
                question_input = st.text_area("Enter your question:", "Please provide a question.")

                submitted = st.form_submit_button('Submit', disabled=not(question_input))
                if submitted:
                    with st.spinner('Calculating...'):
                        response = "Possible Answer"
                        result.append(response)
                        del question_input

                if len(result):
                    st.info(response)

        else:
            st.write("Please upload your File first!")



if __name__ == "__main__":
    main()