from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

def read_pdfs() -> list[Document]:
    data_path = "./data"
    print('Reading files from', data_path)
    
    document_loader = PyPDFDirectoryLoader(data_path)
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