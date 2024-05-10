from enum import Enum
from dotenv import load_dotenv, find_dotenv
import requests
import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
import json
from service.etc.output_classes import Questions, ChunkSummary, PolicySummary


class LanguageModel(Enum):
    LLAMA2 = "llama2"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo"

class LanguageModelConnection:
    def __init__(self, model:LanguageModel, key:str|None = None):
        self.model = model
        self.key = key
         # Load prompts from external JSON file
        with open('service/etc/prompts.json', 'r') as f:
            self.prompts = json.load(f)

        if model == LanguageModel.LLAMA2:
                load_dotenv(find_dotenv())
                self.ol_url = os.environ.get("OLLAMA_URL")
                self.model_url = self.ol_url+'/api/generate'
                self.llm = Ollama(model=LanguageModel.LLAMA2, base_url=self.ol_url, max_tokens=-1, temperature=0.2)
        elif model == LanguageModel.GPT_3_5:
                self.model_url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'
                self.llm = ChatOpenAI(openai_api_key=self.key, temperature=0.2)
        elif model == LanguageModel.GPT_4:  
                self.model_url = 'https://api.openai.com/v1/engines/gpt-4-turbo/completions'
                self.llm = ChatOpenAI(openai_api_key=self.key, model=LanguageModel.GPT_4.value, temperature=0.2)

    def generate_questionnaire(self, document_chunk):
        # A query intented to prompt a language model to populate the data structure.
        question_query = self.prompts['questionnaire']

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=Questions)

        prompt = PromptTemplate(
        template="The part of the document is {chunk}.\n{format_instructions}\n{query}\n",
        input_variables=["query", "chunk"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        result = chain.invoke({"query": question_query, "chunk": document_chunk})
        return result
    
    def generate_chunk_summary(self, text_chunk):
        # A query intented to prompt a language model to populate the data structure.
        sum_query = self.prompts['chunk_summary']

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=ChunkSummary)

        prompt = PromptTemplate(
        template="{format_instructions}\n {query}\n The Chunk: {text_chunk}\n",
        input_variables=["query", "text_chunk"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        result = chain.invoke({"query": sum_query, "text_chunk": text_chunk})
        return result
    
    def generate_policy_summary(self, chunk_summarys):
        partial_summary = ""
        # A query intented to prompt a language model to populate the data structure.
        sum_query = self.prompts['full_summary']

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=PolicySummary)

        prompt = PromptTemplate(
        template="{format_instructions}\n {query}\n The Chunk summary: {chunk_summary}\n The partial summary: {partial_summary}\n",
        input_variables=["query", "chunk_summary", "partial_summary"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        for chunk_summary in chunk_summarys:
            result = chain.invoke({"query": sum_query, "chunk_summary": chunk_summary, "partial_summary": partial_summary})
            partial_summary += result["summary"]
        return result