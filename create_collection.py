import argparse
from dotenv import load_dotenv
from pdf_tools import read_pdfs, split_documents
from db_tools import add_to_chroma, clear_database


load_dotenv()

def main():
    # Check if the database should be reset (using the --reset flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    documents = read_pdfs()
    if not documents:
        print('No documents parsed, exiting.')
        return    
   
    chunked_documents = split_documents(documents)

    print('Creating collection from documents')
    add_to_chroma(chunked_documents)

if __name__ == "__main__":
    main()