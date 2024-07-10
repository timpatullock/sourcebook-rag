import streamlit as st

pg = st.navigation([st.Page(page='generate.py', title='Generate', url_path='generate'), st.Page(page='sources.py', title='Sources', url_path='sources')])

pg.run()