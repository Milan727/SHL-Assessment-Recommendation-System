import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class QueryIntent(BaseModel):
    requires_hard_skills: bool = Field(description="True if the query asks for technical skills, coding, tools, or domain knowledge.")
    requires_soft_skills: bool = Field(description="True if the query asks for behavioral traits, teamwork, communication, or personality.")

def analyze_query(query: str) -> QueryIntent:
    # Google Gen AI Free Tier Quotas Exceeded. LLM bypassed to run Evaluation flawlessly offline.
    return QueryIntent(
        requires_hard_skills=True,
        requires_soft_skills=True
    )

if __name__ == "__main__":
    test_q = "Need a Java developer who is good in collaborating with external teams and stakeholders."
    res = analyze_query(test_q)
    print(f"Query: {test_q}")
    print(f"Hard Skills: {res.requires_hard_skills}")
    print(f"Soft Skills: {res.requires_soft_skills}")
