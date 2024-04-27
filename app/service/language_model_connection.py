from enum import Enum
from dotenv import load_dotenv, find_dotenv
import requests
import os
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import OpenAI


class LanguageModel(Enum):
    LLAMA2 = "llama2"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo"

class Question(BaseModel):
    Question: str = Field(description="question to check the knowledge level")
    answers: list = Field(description="list of 4 possible answers, only one is correct, include A, B, C, D before question")
    correct_answer: str = Field(description="correct answer")

class Questions(BaseModel):
    Questions: List[Question] = Field(description="question object")

class LanguageModelConnection:
    def __init__(self, model:LanguageModel, key:str|None = None):
        self.model = model
        self.key = key

        if model == LanguageModel.LLAMA2:
                load_dotenv(find_dotenv())
                self.ol_url = os.environ.get("OLLAMA_URL")
                self.model_url = self.ol_url+'/api/generate'
        elif model == LanguageModel.GPT_3_5:
                self.model_url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'
        elif model == LanguageModel.GPT_4:  
                self.model_url = 'https://api.openai.com/v1/engines/gpt-4-turbo/completions'

    def generate_questionnaire(self, topic):
        # A query intented to prompt a language model to populate the data structure.
        question_query = "Your job is to determine the level of knowledge of a user. Given a topic ask 2 multiple choice questions with 4 possible answers each, that help to determine the knowledge level."

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=Questions)

        prompt = PromptTemplate(
        template="The topic is {topic}.\n{format_instructions}\n{query}\n",
        input_variables=["query", "topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        if self.model == LanguageModel.GPT_3_5:
                llm = OpenAI(openai_api_key=self.key)
        else:
                llm = OpenAI(openai_api_key=self.key)

        chain = prompt | llm | parser

        result = chain.invoke({"query": question_query, "topic": topic})
        return result