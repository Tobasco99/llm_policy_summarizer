import streamlit as st
import streamlit_scrollable_textbox as stx

dummy = "REGULATION (EU) 2019/2144 \nThe regulation mandates that all new vehicles and their components meet stringent safety and environmental standards through type-approval. It defines specific systems and components like tyre pressure monitors and intelligent speed assistance, ensuring they adhere to detailed technical specifications. Vehicle manufacturers are responsible for compliance, which aims to enhance the safety of vehicle occupants and vulnerable road users, while also integrating advanced vehicle systems across all motor vehicle categories. The regulation mandates that all new vehicles and their components meet stringent safety and environmental standards through type-approval. It defines specific systems and components like tyre pressure monitors and intelligent speed assistance, ensuring they adhere to detailed technical specifications. Vehicle manufacturers are responsible for compliance, which aims to enhance the safety of vehicle occupants and vulnerable road users, while also integrating advanced vehicle systems across all motor vehicle categories. Additionally, the policy focuses on enhancing vehicle safety through advanced systems like driver drowsiness detection, event data recorders, and emergency response systems. These systems are designed to protect data privacy, prevent misuse, and improve road safety for all users, including vulnerable groups. Manufacturers are required to comply with strict data handling and system design regulations to ensure both safety and privacy. Key systems such as advanced emergency braking and lane-keeping are mandated to be non-deactivatable and must provide reliable operation. Event data recorders are required to record specific data such as vehicle speed and safety system status during collisions and must be designed to protect data against misuse. Regulations specify that data from event recorders can only be used for accident research and must comply with privacy regulations. Vehicles must also be designed to enhance visibility of vulnerable road users and to be accessible by persons with reduced mobility. The regulation mandates that all new vehicles and their components meet stringent safety and environmental standards through type-approval. It defines specific systems and components like tyre pressure monitors and intelligent speed assistance, ensuring they adhere to detailed technical specifications. Vehicle manufacturers are responsible for compliance, which aims to enhance the safety of vehicle occupants and vulnerable road users, while also integrating advanced vehicle systems across all motor vehicle categories. Additionally, the policy focuses on enhancing vehicle safety through advanced systems like driver drowsiness detection, event data recorders, and emergency response systems. These systems are designed to protect data privacy, prevent misuse, and improve road safety for all users, including vulnerable groups. Manufacturers are required to comply with strict data handling and system design regulations to ensure both safety and privacy. Key systems such as advanced emergency braking and lane-keeping are mandated to be non-deactivatable and must provide reliable operation. Event data recorders are required to record specific data such as vehicle speed and safety system status during collisions and must be designed to protect data against misuse. Regulations specify that data from event recorders can only be used for accident research and must comply with privacy regulations. Vehicles must also be designed to enhance visibility of vulnerable road users and to be accessible by persons with reduced mobility. The Commission is set to adopt implementing and delegated acts to establish uniform procedures and technical specifications for hydrogen-powered and automated vehicles, with significant involvement from the European Parliament, Council, and Member States. These regulations aim to enhance vehicle safety and compliance, supported by regular evaluations and reports on the implementation progress. Stakeholders like the Technical Committee - Motor Vehicles play a crucial role in advising and assisting the Commission. The regulation mandates that all new vehicles and their components meet stringent safety and environmental standards through type-approval."

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

    tab1, tab2 = st.tabs(["Summarization", "Ask your policy"])

    with tab1:

                # make the choice of llm to select from a selectbox
        llm = st.sidebar.selectbox("LLM", ["gpt-4-turbo", "gpt-3.5-turbo", "Llama3-8B"])


        st.title("Policy Summarization App")
        #chain_type = st.sidebar.selectbox("Chain Type", ["map_reduce", "refine"])
        chunk_size = st.sidebar.slider("Chunk Size", min_value=200, max_value=100000, step=100, value=4000)
        chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=100, max_value=10000, step=100, value=200)
        change = st.sidebar.toggle("Change Prompt")

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
                preference = st.text_area("Special requests", "e.g. Focus on safety and environmental standards.")

                if st.button("Summarize"):
                    #result = custom_summary(docs,llm, user_prompt, chain_type)
                    st.info("Summarization successfull")
                    st.info("Linked Policies: 631/2009, 406/2010, 672/2010, 1003/2010, 1005/2010, 1008/2010, 1009/2010, 19/2011, 109/2011, 458/2011, 65/2012, 130/2012, 347/2012, 351/2012, 1230/2012")
                    st.text_area("Summary:",dummy, height=400)
                    
                    col1, col2, col3, col4 = st.columns([1,1,1,1])

                    with col1:
                        c1, c2 = st.columns([1,1])
                        with c1:
                            st.button('Print')
                        with c2:
                            st.button('Download')

    with tab2:
        st.text_input("Enter your question", value="What are type safety regulations?")
        st.button("Ask")
        st.text_area("Answer", value=dummy)
                    



if __name__ == "__main__":
    main()