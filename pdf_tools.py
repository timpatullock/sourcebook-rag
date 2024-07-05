import os
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

def read_pdfs() -> list[Document]:
    pdf_folder_path = "./data"
    print('Reading files from', pdf_folder_path)
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            print('Reading', file)
            
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    return documents