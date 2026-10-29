
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Model used to convert text into embeddings.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Persistent vector database stored locally.
vector_store = Chroma(
    collection_name="schema_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Database schema descriptions and examples.
documents = [
    """
    Table: employees
    Columns: id, name, department_id, salary.
    Stores employee information, including salary.
    department_id references departments.id.
    """,
    """
    Table: departments
    Columns: id, department_name.
    Stores department names such as IT and HR.
    The departments table is related to employees
    through employees.department_id.
    """,
    """
    Example question: Find the average salary in IT.
    SQL concept: Join employees and departments,
    filter department_name = IT, and use AVG(salary).
    """
]


def initialize_vector_store():
    # Avoid adding duplicate copies on each execution.
    existing = vector_store.get()
    existing_count = len(existing.get("ids", []))

    if existing_count == 0:
        vector_store.add_texts(
            texts=documents,
            ids=[
                "employees_schema",
                "departments_schema",
                "average_salary_example"
            ]
        )
        print("Schema documents added to ChromaDB.")
    else:
        print("ChromaDB already contains schema documents.")


def retrieve_context(question):
    results = vector_store.similarity_search(
        question,
        k=3
    )

    return "\n\n".join(
        document.page_content for document in results
    )


if __name__ == "__main__":
    initialize_vector_store()

    question = input("Enter a database question: ")

    print("\nRetrieved context:")
    print(retrieve_context(question))

