
import streamlit as st
import chromadb
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import dotenv_values
from pdf_tools import read_pdfs


os.environ['OPENAI_API_KEY'] = dotenv_values('.env')['OPENAI_API_KEY'] # type: ignore

def create_agent_chain():
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(model_name=model_name) # type: ignore
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def update_collection():
    documents = read_pdfs()
    if not documents:
        print('No documents parsed, continuing.')
        return
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    client = chromadb.HttpClient(host='localhost', port=8000)
    embeddings = OpenAIEmbeddings()

    db = Chroma(client=client, collection_name='sourcebooks', embedding_function=OpenAIEmbeddings())

    db.add_documents(documents=chunked_documents, client=client, collection_name='sourcebooks', embedding=embeddings)


def get_llm_response(query):
    chain = create_agent_chain()
    client = chromadb.HttpClient(host='localhost', port=8000)
    vectordb = Chroma(client=client, collection_name='sourcebooks', embedding_function=OpenAIEmbeddings())

    #vectordb = Chroma(persist_directory="./chroma-store", embedding_function=OpenAIEmbeddings())
    matching_docs = vectordb.similarity_search(query)
    answer = chain.run(input_documents=matching_docs, question=query)
    return answer


# Streamlit UI
# ===============
st.set_page_config(page_title="Doc Searcher", page_icon=":robot:")
st.header("Query PDF Source")

form_input = st.text_input('Enter Query')
submit = st.button("Generate")
update = st.button("Update")

if submit:
    st.write(get_llm_response(form_input))
if update:
    update_collection()