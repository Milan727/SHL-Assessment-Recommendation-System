import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class QueryIntent(BaseModel):
    requires_hard_skills: bool = Field(description="True if the query asks for technical skills, coding, tools, or domain knowledge.")
    requires_soft_skills: bool = Field(description="True if the query asks for behavioral traits, teamwork, communication, or personality.")

def analyze_query(query: str) -> QueryIntent:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
        )
        structured_llm = llm.with_structured_output(QueryIntent)
        
        prompt = PromptTemplate.from_template(
            "Analyze the following job description or query. "
            "Determine if it requires hard/technical skills (coding, domain knowledge, tools) "
            "and/or soft/behavioral skills (communication, teamwork, leadership, personality). "
            "Query: {query}"
        )
        
        chain = prompt | structured_llm
        result = chain.invoke({"query": query})
        return result
    except Exception as e:
        print(f"LLM analysis error (defaulting to balanced): {e}")
        # Fallback: assume both if LLM fails
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
