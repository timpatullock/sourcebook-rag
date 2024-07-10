
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from db_tools import get_db

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item


def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))


def stripChunksFromId(id: str):
    return id.split(':')[0]


def getIds():
    return 0


load_dotenv()


def create_agent_chain():
    model = "gpt-3.5-turbo"
    llm = ChatOpenAI(model=model)
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain


def get_llm_response(query):
    if not query:
        return 'Please provide a query'
    
    if "Fireball" in query:
        return "Cast that motherfucker"
    
    chain = create_agent_chain()
    vectordb = get_db()
    matching_docs = vectordb.similarity_search(query)
    answer = chain.invoke({"input_documents": matching_docs, "question": query})
    return answer['output_text']


# Streamlit UI
# ===============

st.set_page_config(page_title="Doc Searcher", page_icon=":robot:")
st.header("Query PDF Source")

form_input = st.text_input('Enter Query')
generate = st.button("Generate")
result = st.text('')

if generate:
    result.text(get_llm_response(form_input))


