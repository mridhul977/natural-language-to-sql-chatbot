
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from rag import initialize_vector_store, retrieve_context

load_dotenv()

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a MySQL query generator.

Use the database context below to generate one read-only
MySQL SELECT query that answers the user's question.

Rules:
- Use only the tables and columns in the context.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER,
  CREATE, or other data-modifying statements.
- Do not invent table or column names.
- Return only the SQL query, without Markdown code fences.
- If the question cannot be answered using the context,
  do not invent a query.

Database context:
{context}

Question:
{question}

SQL query:
""")

chain = prompt | llm

def generate_sql(question):
    initialize_vector_store()
    context = retrieve_context(question)

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content.strip()

if __name__ == "__main__":
    question = input("Enter your question: ")
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)
