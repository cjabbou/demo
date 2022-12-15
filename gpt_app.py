import app
import streamlit as st

# FIle Processing Packages
from PIL import Image
import pandas as pd
import docx2txt
# import textract # similar to docx2txt
import pdfplumber 
from PyPDF2 import PdfFileReader

st.set_page_config(page_title="GPT-3", page_icon=":shark:", layout="wide")

app.main()
