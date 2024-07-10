from pdf_tools import read_pdfs, split_documents, read_uploaded_pdfs
from db_tools import add_to_chroma
from dotenv import load_dotenv


load_dotenv()

def main():
    documents = read_pdfs()
    if not documents:
        print('No documents parsed, exiting.')
        return    
   
    chunked_documents = split_documents(documents)

    print('Updating collection with documents')
    add_to_chroma(chunked_documents)

def add_uploaded_files(files):
    documents = read_uploaded_pdfs(files)

    if not documents:
        print('No documents found, continuing.')
        return

    chunked_documents = split_documents(documents)
    add_to_chroma(chunked_documents)

if __name__ == "__main__":
    main()