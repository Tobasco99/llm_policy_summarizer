from enum import Enum
from dotenv import load_dotenv, find_dotenv
import requests
import os


class LanguageModel(Enum):
    LLAMA2 = "llama2"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo"

class languageModelConnection:
    def __init__(self, model:LanguageModel, key:str|None = None):
        self.model = model
        self.key = key

        if model == LanguageModel.LLAMA2:
                load_dotenv(find_dotenv())
                self.ol_url = os.environ.get("OLLAMA_URL")
                self.model_url = self.ol_url+'/api/generate'

    def generate_abstract(self, text):
        if self.model == LanguageModel.LLAMA2:
            body = {'model': 'llama2',
                    'prompt': f"Give me a summary of the key regulations described in this policy document:{text}",
                    'stream': False}  
            response = requests.post(self.model_url, json=body)
            abstract = response.json()["response"]
            return abstract

