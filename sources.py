from db_tools import removeSourceFromDB, getUniqueSources
from update_collection import add_uploaded_files
import os
import streamlit as st

st.header('Upload Sources')
uploaded_files = st.file_uploader('Pick a PDF', type="pdf", accept_multiple_files=True)
submit = st.button('Submit Files')

st.header('Sources')

for source in getUniqueSources():
    button = st.button(f'Delete "{os.path.basename(source)}"' )
    if button:
        chunks = removeSourceFromDB(source)

if submit and uploaded_files:
    add_uploaded_files(uploaded_files)