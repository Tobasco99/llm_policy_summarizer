from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class Question(BaseModel):
    question: str = Field(description="question to check the level of understanding")
    answers: list = Field(description="list of 4 possible answers, only one is correct, include A, B, C, D before question")
    correct_answer: str = Field(description="correct answer")

class Questions(BaseModel):
    questions: List[Question] = Field(description="question object")

class ChunkSummary(BaseModel):
    stakeholder: list = Field(description="list of involved stakeholders, without regulations, institutions or companies or groups of people") 
    key_information: list = Field(description="list of key information as short bulletpoints")
    chunk_summary: str = Field(description="summary of the entire chunk")

class PolicySummary(BaseModel):
    summary: str = Field(description="summary of the policy")

class Answer(BaseModel):
    answer: str = Field(description="answer to the question")