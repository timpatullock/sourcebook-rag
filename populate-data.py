from langchain.vectorstores import Chroma
import os
import chromadb
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import dotenv_values
from chromadb.config import Settings
import uuid

os.environ['OPENAI_API_KEY'] = dotenv_values('.env')['OPENAI_API_KEY'] # type: ignore


def load_chunk_persist_pdf():
    pdf_folder_path = "./data"
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    if not documents:
        print('No documents parsed, continuing.')
        return
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    client = chromadb.HttpClient(host='localhost', port=8000)
    client.reset()  # resets the database

    embeddings = OpenAIEmbeddings()

    db4 = Chroma.from_documents(documents=chunked_documents, client=client, collection_name='sourcebooks', embedding=embeddings)

    #vectordb = Chroma(
    #    documents=chunked_documents,
    #    embedding=OpenAIEmbeddings(),
    #    persist_directory="./chroma-store"
    #)
    #vectordb.persist()

load_chunk_persist_pdf()