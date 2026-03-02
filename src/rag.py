import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from operator import itemgetter

CHROMA_PATH = "data/chroma_db"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    # 1. Init Vector Store & Retriever
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 2. Init LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # 3. Create Prompt
    template = """You are a helpful assistant for SHL Assessment Recommendations.
Use the following retrieved catalog segments to answer the question.
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {input}

Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Build LCEL Chain
    setup_and_retrieval = RunnableParallel(
        {"context": itemgetter("input") | retriever, "input": itemgetter("input")}
    )
    
    answer_chain = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )
    
    rag_chain = setup_and_retrieval.assign(answer=answer_chain)
    return rag_chain

def test_rag():
    rag_chain = get_rag_chain()
    query = "What assessments do you have for Account Managers?"
    print(f"Query: {query}")
    print("-" * 50)
    
    response = rag_chain.invoke({"input": query})
    
    print("Answer:")
    print(response["answer"])
    print("-" * 50)
    print("Sources retrieved:")
    for doc in response["context"]:
        title = doc.metadata.get("title", "N/A")
        url = doc.metadata.get("url", "N/A")
        print(f"- {title} ({url})")

if __name__ == "__main__":
    test_rag()
