
import streamlit as st
import chromadb
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from update_collection import update_collection

load_dotenv()

def create_agent_chain():
    model = "gpt-3.5-turbo"
    llm = ChatOpenAI(model=model)
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain


def get_llm_response(query):
    chain = create_agent_chain()
    client = chromadb.HttpClient(host='localhost', port=8000)
    vectordb = Chroma(client=client, collection_name='sourcebooks', embedding_function=OpenAIEmbeddings())

    matching_docs = vectordb.similarity_search(query)
    answer = chain.invoke({"input_documents": matching_docs, "question": query})
    return answer['output_text']


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