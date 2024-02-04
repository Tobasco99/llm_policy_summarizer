# Description

This repository contains a Python script called policy_summarization_app.py that uses OpenAI GPT models,
to summarize a political policy. The app takes the domain knowledge of the user into account to generate 
a comprehensive summary.
It also provides a refinement of the generated summary, as well as a question answering mechanism.

# Installation

To use the policy_summarization_app.py script, follow the steps:

- Create the conda environment:

```conda env create -f environment.yml```

Or just install the required libraries using the following command:

```pip install -r requirements.txt```

Also make sure that an OpenAI API key is provided as an environment variable called: "OPENAI_API_KEY".

### Running the policy summarization app
In terminal run:

```streamlit run ./custom_summarization_app.py```

# Credits
[langchain](https://python.langchain.com/en/latest/), [streamlit](https://streamlit.io/).

