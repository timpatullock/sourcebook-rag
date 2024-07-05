from langchain.vectorstores import Chroma
import os
import chromadb
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import dotenv_values
from pdf_tools import read_pdfs

os.environ['OPENAI_API_KEY'] = dotenv_values('.env')['OPENAI_API_KEY'] # type: ignore


def create_collection():
    documents =  read_pdfs()
    if not documents:
        print('No documents parsed, continuing.')
        return
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    client = chromadb.HttpClient(host='localhost', port=8000)
    resetSuccessful = client.reset()  # resets the database

    if not resetSuccessful:
        print('Database was not reset successfully!')

    embeddings = OpenAIEmbeddings()

    Chroma.from_documents(documents=chunked_documents, client=client, collection_name='sourcebooks', embedding=embeddings)

create_collection()