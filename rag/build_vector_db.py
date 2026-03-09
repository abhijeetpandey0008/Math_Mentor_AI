import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


KNOWLEDGE_PATH = "rag/knowledge_base"
VECTOR_DB_PATH = "rag/vector_db"


def build_vector_db():

    documents = []

    # Load knowledge base files
    for file in os.listdir(KNOWLEDGE_PATH):

        if file.endswith(".txt"):

            loader = TextLoader(os.path.join(KNOWLEDGE_PATH, file))

            documents.extend(loader.load())


    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)


    # Embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    # Create vector database
    vectordb = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=VECTOR_DB_PATH
    )


    vectordb.persist()

    print("Vector database created successfully!")


if __name__ == "__main__":

    build_vector_db()