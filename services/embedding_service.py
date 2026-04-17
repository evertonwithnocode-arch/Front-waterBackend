from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.chroma_client import get_chroma

def process_document(content, metadata):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(content)

    db = get_chroma(metadata["collection"])

    docs = [
        {
            "page_content": chunk,
            "metadata": metadata
        }
        for chunk in chunks
    ]

    db.add_documents(docs)
    db.persist()

    return {"chunks": len(chunks)}