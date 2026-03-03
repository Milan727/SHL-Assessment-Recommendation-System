import os
import re
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class QueryIntent(BaseModel):
    requires_hard_skills: bool = Field(description="True if the query asks for technical skills, coding, tools, or domain knowledge.")
    requires_soft_skills: bool = Field(description="True if the query asks for behavioral traits, teamwork, communication, or personality.")
    search_keywords: list[str] = Field(description="List of 3-5 critical functional keywords or synonyms for searching a catalog (e.g., 'Leadership', 'Executive', 'Java', 'Sales', 'OPQ', 'Cognitive').")

# Fast keyword-based fallback (no API needed)
HARD_KEYWORDS = re.compile(
    r'\b(java|python|sql|javascript|typescript|c\+\+|c#|\.net|ruby|php|golang|go|rust|swift|kotlin|'
    r'html|css|react|angular|vue|node|django|flask|spring|aws|azure|gcp|docker|kubernetes|'
    r'linux|git|database|mongodb|postgresql|mysql|redis|api|rest|graphql|'
    r'machine learning|deep learning|data science|analytics|algorithm|'
    r'technical|programming|coding|developer|engineer|software|devops|'
    r'sap|salesforce|excel|tableau|power bi|selenium|automation|testing|qa|'
    r'network|security|cloud|infrastructure|embedded|firmware|hardware|'
    r'accounting|finance|math|numerical|quantitative|agile|scrum)\b', re.IGNORECASE
)

SOFT_KEYWORDS = re.compile(
    r'\b(leadership|communication|teamwork|collaborate|interpersonal|'
    r'presentation|negotiation|conflict|emotional|empathy|personality|'
    r'behavioral|behaviour|behavior|soft skills|management|'
    r'customer service|sales|relationship|stakeholder|'
    r'creative|innovation|problem solving|critical thinking|'
    r'adaptability|resilience|integrity|ethics|'
    r'motivation|coaching|mentoring|delegation|'
    r'time management|organization|planning|decision)\b', re.IGNORECASE
)

SYNONYM_MAP = {
    # Executives & Managers
    r'\b(coo|ceo|cto|cfo|executive|director|head|vp)\b': ['leadership', 'executive', 'director', 'management', 'opq', 'personality'],
    r'\b(manager|supervisor|lead)\b': ['manager', 'supervisor', 'leadership', 'management'],
    # Sales & Marketing
    r'\b(sales|account manager|bd|business development|seller)\b': ['sales', 'representative', 'customer', 'negotiation', 'communication'],
    r'\b(marketing|seo|advertising|brand)\b': ['marketing', 'advertising', 'digital', 'communication'],
    # Roles
    r'\b(writer|content|editor|proofread)\b': ['writing', 'english', 'proofreading', 'verbal'],
    r'\b(admin|assistant|clerk|receptionist)\b': ['administrative', 'assistant', 'clerk', 'operations'],
    r'\b(consultant|adviser|advisor)\b': ['consultant', 'adviser', 'sales', 'professional'],
    r'\b(bank|financial|accounting)\b': ['bank', 'finance', 'financial', 'accounting'],
    r'\b(data analyst|data science|analytics|bi)\b': ['data', 'analyst', 'sql', 'analysis', 'ssas'],
    r'\b(javascript|java\s*script|js|typescript|react|angular|node\.?js|express)\b': ['javascript', 'programming', 'software', 'developer'],
    r'\b(java)\b': ['java', 'programming', 'software', 'developer'],
    r'\b(python)\b': ['python', 'programming', 'software', 'developer'],
    r'\b(sql)\b': ['sql', 'database', 'programming', 'software'],
    r'\b(database|mongodb|postgresql|mysql|redis)\b': ['database', 'sql', 'programming'],
    r'\b(developer|engineer|coder|programmer)\b': ['programming', 'software', 'developer', 'engineer'],
    # Levels
    r'\b(graduate|entry|junior|fresher|university)\b': ['entry', 'graduate', 'junior', 'fundamental'],
    # Assessments
    r'\b(cognitive|reasoning|interactive|aptitude)\b': ['verify', 'interactive', 'reasoning', 'cognitive', 'numerical'],
}

def _keyword_fallback(query: str) -> QueryIntent:
    """Fast, zero-API-call intent detection using semantic synonym dictionary."""
    has_hard = bool(HARD_KEYWORDS.search(query))
    has_soft = bool(SOFT_KEYWORDS.search(query))
    
    # Default to both if no keywords match
    if not has_hard and not has_soft:
        has_hard = True
        has_soft = True
        
    query_lower = query.lower()
    search_keywords = ["assessment"]
    
    # Extract robust keywords using synonym mapping
    mapped_keywords = []
    for pattern, synonyms in SYNONYM_MAP.items():
        if re.search(pattern, query_lower):
            mapped_keywords.extend(synonyms)
            
    if mapped_keywords:
        # Get unique words preserving order
        seen = set()
        search_keywords = [x for x in mapped_keywords if not (x in seen or seen.add(x))]
    else:
        # Generic word fallback
        words = [w for w in re.findall(r'\b\w+\b', query) if len(w) > 4]
        if words:
            search_keywords = list(set(words[:5]))
            
    return QueryIntent(requires_hard_skills=has_hard, requires_soft_skills=has_soft, search_keywords=search_keywords)

# Circuit breaker: skip LLM calls after first failure
_llm_available = True

def analyze_query(query: str) -> QueryIntent:
    global _llm_available
    
    if not _llm_available:
        return _keyword_fallback(query)
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
            timeout=10,
        )
        structured_llm = llm.with_structured_output(QueryIntent)
        
        prompt = PromptTemplate.from_template(
            "Analyze the following job description or query. "
            "1. Determine if it requires hard/technical skills and/or soft/behavioral skills. "
            "2. Extract or generate 3-5 critical search keywords/synonyms to find matching assessments "
            "(e.g., if 'COO', generate 'Leadership', 'Executive', 'Management'). "
            "Query: {query}"
        )
        
        chain = prompt | structured_llm
        result = chain.invoke({"query": query})
        return result
    except Exception as e:
        print(f"GEMINI API ERROR: {e}")
        _llm_available = False
        return _keyword_fallback(query)

if __name__ == "__main__":
    test_q = "Need a Java developer who is good in collaborating with external teams and stakeholders."
    res = analyze_query(test_q)
    print(f"Query: {test_q}")
    print(f"Hard Skills: {res.requires_hard_skills}")
    print(f"Soft Skills: {res.requires_soft_skills}")
