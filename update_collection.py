from langchain_text_splitters import CharacterTextSplitter
from pdf_tools import read_pdfs
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

def update_collection():
    documents = read_pdfs()
    if not documents:
        print('No documents parsed, continuing.')
        return
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    print('Chunking documents')
    chunked_documents = text_splitter.split_documents(documents)
    print('Chunking complete')
    client = chromadb.HttpClient(host='localhost', port=8000)
    embeddings = OpenAIEmbeddings()

    db = Chroma(client=client, collection_name='sourcebooks', embedding_function=OpenAIEmbeddings())

    print('Adding documents to store')

    db.add_documents(documents=chunked_documents, client=client, collection_name='sourcebooks', embedding=embeddings)

    print('Successfully added documents to store')

