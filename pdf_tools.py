from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import os
from pathlib import Path

def read_pdfs(location: str = 'data') -> list[Document]:
    print('Reading files from', location)
    
    document_loader = PyPDFDirectoryLoader(location)
    return document_loader.load()

def split_documents(documents) -> list[Document]:
    text_splitter = CharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False
        )
    print('Chunking documents')
    chunked_documents = text_splitter.split_documents(documents)
    print('Chunking complete')
    return chunked_documents

def calculate_chunk_ids(chunks: list[Document]) -> list[Document]:

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    return chunks
        
def read_uploaded_pdfs(uploaded_files: list) -> list[Document]:
    # Create the temp directory if it doesn't already exist
    print('Reading new files')
    Path(f'{os.path.curdir}/tmp').mkdir(exist_ok=True)

    documents: list[Document] = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            print(f'Reading {uploaded_file.name}')
            # Create file in tmp directory to be read by the PDF loader, this is inherently dangerous on a public platform
            # if a safer version exists (eg. reads parses directly from the blob), that would be fantastic
            file_location = f'tmp/{uploaded_file.name}'
            with open(file_location, mode='wb') as w:
                w.write(uploaded_file.getvalue())
            loader = PyPDFLoader(file_location)
            documents.extend(loader.load())
            # delete the generated file
            os.remove(file_location)
            
    return documents

        