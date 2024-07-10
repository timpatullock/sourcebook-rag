import os
import shutil
from langchain_community.vectorstores import Chroma
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from pdf_tools import calculate_chunk_ids

CHROMA_DEFAULT_PATH = 'chroma'
CHROMA_DEFAULT_HOST = 'localhost'
CHROMA_DEFAULT_PORT = 8000
CHROMA_DEFAULT_COLLECTION = 'sourcebooks'

def get_db() -> Chroma:
    useServer = os.getenv('USE_CHROMA_SERVER')
    chromaCollection = os.getenv('CHROMA_COLLECTION') or CHROMA_DEFAULT_COLLECTION
    chromaPath = os.getenv('CHROMA_PATH') or CHROMA_DEFAULT_PATH
    chromaHost = os.getenv('CHROMA_HOST') or CHROMA_DEFAULT_HOST
    chromaPort = int(os.getenv('CHROMA_PORT') or CHROMA_DEFAULT_PORT)

    if useServer:
        client = chromadb.HttpClient(host=chromaHost, port=chromaPort)
        return Chroma(client=client, collection_name=chromaCollection, embedding_function=OpenAIEmbeddings())    
    else: 
        return Chroma(persist_directory=chromaPath, collection_name=chromaCollection, embedding_function=OpenAIEmbeddings())
    
def clear_database():
    useServer = os.getenv('USE_CHROMA_SERVER')
    chromaHost = os.getenv('CHROMA_HOST') or CHROMA_DEFAULT_HOST
    chromaPort = int(os.getenv('CHROMA_PORT') or CHROMA_DEFAULT_PORT)
    chromaPath = os.getenv('CHROMA_PATH') or CHROMA_DEFAULT_PATH

    if useServer:
        client = chromadb.HttpClient(host=chromaHost, port=chromaPort)
        client.reset()

    else:        
        if os.path.exists(chromaPath):
            shutil.rmtree(chromaPath)

    
def add_to_chroma(chunks: list[Document]):
    useServer = os.getenv('USE_CHROMA_SERVER')
    db = get_db()

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)
    
    
    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        
        if not useServer:
            print('Persisting changes to file')
            db.persist()
            print('Persisted')
    else:
        print("✅ No new documents to add")

def remove_from_chroma(ids_to_delete: list[str]): 
    db = get_db()
    db.delete(ids=ids_to_delete)

    useServer = os.getenv('USE_CHROMA_SERVER')

    if not useServer:
        print('Persisting changes to file')
        db.persist()
        print('Persisted')

def removeSourceFromDB(source: str):
    vectordb = get_db()
    results = vectordb.get(where={'source':source})['ids']
    remove_from_chroma(results)

def getUniqueSources() -> list[str]:
    vectordb = get_db()
    ids = vectordb.get(include=['metadatas'])
    sources = []
    for metadata in ids['metadatas']: 
        if metadata['source'] not in sources:
            sources.append(metadata['source'])

    return sources