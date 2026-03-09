from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


VECTOR_DB_PATH = "rag/vector_db"


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load vector database
vector_db = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embeddings
)


# Create retriever
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


def retrieve_docs(query):

    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        results.append(doc.page_content)

    return results