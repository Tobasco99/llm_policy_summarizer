import streamlit as st


def custom_summary(docs,llm, custom_prompt, chain_type):
    return "This is a generated Summary"

@st.cache_data
def setup_documents(pdf_file_path, chunk_size, chunk_overlap):
    pass


@st.cache_data
def color_chunks(text: str, chunk_size: int, overlap_size: int) -> str:
    overlap_color = "#808080" # Light gray for the overlap
    chunk_colors = ["#a8d08d", "#c6dbef", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2"] # Different shades of green for chunks

    colored_text = ""
    overlap = ""
    color_index = 0

    for i in range(0, len(text), chunk_size-overlap_size):
        chunk = text[i:i+chunk_size]
        if overlap:
            colored_text += f'<mark style="background-color: {overlap_color};">{overlap}</mark>'
        chunk = chunk[len(overlap):]
        colored_text += f'<mark style="background-color: {chunk_colors[color_index]};">{chunk}</mark>'
        color_index = (color_index + 1) % len(chunk_colors)
        overlap = text[i+chunk_size-overlap_size:i+chunk_size]

    return colored_text


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
            on = st.toggle('Domain knowledge?')

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
                    result = custom_summary(docs,llm, user_prompt, chain_type)
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