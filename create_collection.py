import os
import chromadb
from dotenv import dotenv_values
from pdf_tools import read_pdfs
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

os.environ['OPENAI_API_KEY'] = dotenv_values('.env')['OPENAI_API_KEY'] # type: ignore


def create_collection():
    documents = read_pdfs()
    if not documents:
        print('No documents parsed, continuing.')
        return
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    print('Chunking documents')
    chunked_documents = text_splitter.split_documents(documents)
    print('Chunking complete')
    client = chromadb.HttpClient(host='localhost', port=8000)
    resetSuccessful = client.reset()  # resets the database

    if not resetSuccessful:
        print('Database was not reset successfully!')
    
    print('Creating collection from documents')
    Chroma.from_documents(documents=chunked_documents, client=client, collection_name='sourcebooks', embedding=OpenAIEmbeddings())
    print('Collection Created')

create_collection()