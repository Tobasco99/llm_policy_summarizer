from enum import Enum
from dotenv import load_dotenv, find_dotenv
import requests
import os
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import OpenAI
from langchain_community.llms import Ollama


class LanguageModel(Enum):
    LLAMA2 = "llama2"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo"

class Question(BaseModel):
    question: str = Field(description="question to check the knowledge level")
    answers: list = Field(description="list of 4 possible answers, only one is correct, include A, B, C, D before question")
    correct_answer: str = Field(description="correct answer")

class Questions(BaseModel):
    questions: List[Question] = Field(description="question object")

class ChunkSummary(BaseModel):
    stakeholder: list = Field(description="list of involved stakeholders") 
    key_information: list = Field(description="list of key information as short bulletpoints")
    chunk_summary: str = Field(description="summary of the entire chunk")

class LanguageModelConnection:
    def __init__(self, model:LanguageModel, key:str|None = None):
        self.model = model
        self.key = key

        if model == LanguageModel.LLAMA2:
                load_dotenv(find_dotenv())
                self.ol_url = os.environ.get("OLLAMA_URL")
                self.model_url = self.ol_url+'/api/generate'
                self.llm = Ollama(model=LanguageModel.LLAMA2, base_url=self.ol_url)
        elif model == LanguageModel.GPT_3_5:
                self.model_url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'
                self.llm = OpenAI(openai_api_key=self.key, max_tokens=-1, temperature=0.2)
        elif model == LanguageModel.GPT_4:  
                self.model_url = 'https://api.openai.com/v1/engines/gpt-4-turbo/completions'
                self.llm = OpenAI(openai_api_key=self.key, model=LanguageModel.GPT_4, max_tokens=-1, temperature=0.2)

    def generate_questionnaire(self, topic):
        # A query intented to prompt a language model to populate the data structure.
        question_query = "Your job is to determine the level of knowledge of a user. Given a topic ask 3 multiple choice questions with 4 possible answers each, that help to determine the knowledge level."

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=Questions)

        prompt = PromptTemplate(
        template="The topic is {topic}.\n{format_instructions}\n{query}\n",
        input_variables=["query", "topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        result = chain.invoke({"query": question_query, "topic": topic})
        return result
    
    def generate_chunk_summary(self, text_chunk):
        # A query intented to prompt a language model to populate the data structure.
        sum_query = "Given the part of a policy document, extract useful information and generate a summary. If a external regulation is mentioned, it is wrapped in reg tags with description of it in reg_desc tags. To effectively complete the summarization, follow these steps: 1. extract the key information provided in the text and write all information as bullet points in the key_information key. 2. identify the stakeholder involved in the text and write it in the stakeholder key. 3. use the key information and the stakeholder to generate a summary of the text and write it in the chunk_summary key."

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