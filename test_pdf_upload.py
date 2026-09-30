import streamlit as st

from components.pdf.pdf_upload import show_pdf_upload

st.set_page_config(page_title="PDF Upload Test")

show_pdf_upload("demo@gmail.com")