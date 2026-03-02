import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class QueryIntent(BaseModel):
    requires_hard_skills: bool = Field(description="True if the query asks for technical skills, coding, tools, or domain knowledge.")
    requires_soft_skills: bool = Field(description="True if the query asks for behavioral traits, teamwork, communication, or personality.")

def analyze_query(query: str) -> QueryIntent:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(QueryIntent)
    
    prompt = f"Analyze the following job description or search query and determine if it requires hard technical skills, soft behavioral skills, or both.\n\nQuery: {query}"
    
    result = structured_llm.invoke(prompt)
    return result

if __name__ == "__main__":
    test_q = "Need a Java developer who is good in collaborating with external teams and stakeholders."
    res = analyze_query(test_q)
    print(f"Query: {test_q}")
    print(f"Hard Skills: {res.requires_hard_skills}")
    print(f"Soft Skills: {res.requires_soft_skills}")
