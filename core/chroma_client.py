from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from config import CHROMA_PATH

def get_chroma(collection_name):
    return Chroma(
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )