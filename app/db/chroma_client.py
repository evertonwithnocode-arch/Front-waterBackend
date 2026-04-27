import chromadb

client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="./chroma_db"
    )
)

collection = client.get_or_create_collection(name="rag_collection")