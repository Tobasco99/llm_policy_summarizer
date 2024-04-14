from textwrap import dedent


def get_prompt_map_chunk(text_chunk):
    """
    Generate a prompt for mapping a text chunk to useful information and generating a summary.

    Args:
        text_chunk (str): The part of a policy document separated by <>.

    Returns:
        str: The generated prompt.
    """
    prompt = dedent("""\
                Given the part of a policy document separated by <>, extract useful information and generate a summary. 
                Format your response as JSON with the following structure:
                {
                    "stakeholder": Stakeholder involved,
                    "key_information": ["information 1", "information 2", "information 3"],
                    "chunk_summary": Chunk summary,
                }
                To effectively complete the summarization, follow these steps:
                - First, extract the key information provided in the text and write all information in the key_information key.
                - Second, identify the stakeholder involved in the text and write it in the stakeholder key.
                - Finally, use the key information and the stakeholder to generate a summary of the text and write it in the chunk_summary key.
                """)

    prompt += f"{text_chunk}"

    return prompt