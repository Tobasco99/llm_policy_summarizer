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

            # make the choice of llm to select from a selectbox
    llm = st.sidebar.selectbox("LLM", ["gpt-4-turbo", "gpt-3.5-turbo", "Llama3-8B"])

    st.title("Policy Summarization App")
    #chain_type = st.sidebar.selectbox("Chain Type", ["map_reduce", "refine"])
    chunk_size = st.sidebar.slider("Chunk Size", min_value=200, max_value=100000, step=100, value=4000)
    chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=100, max_value=10000, step=100, value=200)
    preference = st.sidebar.text_area("Special requests", "e.g. Focus on safety and environmental standards.")
    #temperature = st.sidebar.number_input("LLM Temperature", min_value=0.0, max_value=1.0, step=0.1, value=0.0)



    uploaded_file = st.file_uploader(label='Choose your policy document', type=['pdf', 'docx'])
    #user_prompt = st.text_input("Enter custom summarization requests")
    if uploaded_file is not None:
        df = "file"
        #on = st.toggle('Domain knowledge?')

        if uploaded_file != None:
            docs = setup_documents(uploaded_file, chunk_size, chunk_overlap)
            st.info("Policy was loaded successfully")
            st.info(" The Policy is about Regulatory Requirements for Vehicle and Tyre Type-Approval: Safety, Efficiency, and Environmental Standards")
            knowledge = st.select_slider("Select your Domain Knowledge", options=["None", "Basic", "Expert"])

            if st.button("Summarize"):
                #result = custom_summary(docs,llm, user_prompt, chain_type)
                st.info("Summarization successfull")
                
                col1, col2, col3, col4 = st.columns([1,1,1,1])

                with col1:
                    c1, c2 = st.columns([1,1])
                    with c1:
                        st.button('Print')
                    with c2:
                        st.button('Download')

                refine_request = st.text_area("Adjust Summary", "This is a text area to enter possible feedback for a new summary.")
                st.button("Re-generate")
                    



if __name__ == "__main__":
    main()