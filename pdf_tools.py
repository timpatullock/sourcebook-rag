import os
from langchain.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def read_pdfs() -> list[Document]:
    pdf_folder_path = "./data"
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    return documents