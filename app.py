import streamlit as st # Web App
import pandas as pd # Dataframe
import docx2txt # Word
import pdfplumber # PDF
import pytesseract # OCR
import easyocr as ocr  #OCR
import numpy as np #Image Processing 


from PIL import Image # Image
from PyPDF2 import PdfFileReader # PDF
from model import GeneralModel # GPT-3
from pytesseract import pytesseract # OCR
from pytesseract import Output # OCR


# pytesseract.pytesseract.tesseract-ocr == '/usr/share/tesseract-ocr/4.00/tessdata'


#Load Images # Not necessary to use this function
@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Can comment out PyPDF2 function if using pdfplumber
@st.cache
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()
    return all_page_text

#OCR
@st.cache
def display_text(bounds):
    text = []
    for x in bounds:
        t = x[1]
        text.append(t)
    text = ' '.join(text)
    return text 

#image processing
@st.cache
def load_model():
    reader = ocr.Reader(['en'], model_storage_directory='.', download_enabled=True)
    return reader


def main():
    st.title("Audit AI")

    menu = ["DocumentFiles", "Image", "Dataset", "TextAnalyzer", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "DocumentFiles":
        st.subheader("DocumentFiles")
        doc_file = st.file_uploader("Drag or Select Document", type=['pdf', 'docx', 'txt'])
        if st.button("Process"):
            if doc_file is not None:
                # st.write(type(doc_file))
                # st.write(dir(doc_file))
                files_details = {"FileName":doc_file.name,">>FileType":doc_file.type,"FileSize(Byte)":doc_file.size}
                st.write(files_details)
                if doc_file.type == "text/plain":
                    st.success("Text File Uploaded")
                    raw_text = str(doc_file.read(), "utf-8")
                    st.write(raw_text) # different format than text
                    # st.text(raw_text) # different format than write
                elif doc_file.type == "application/pdf":
                    st.success("PDF Uploaded")
                    # try: # using pdfplumber
                    #     pdf = pdfplumber.open(doc_file)
                    #     page = pdf.pages[0]
                    #     raw_text = page.extract_text()
                    #     st.write(raw_text)
                    #     # st.text(raw_text)
                    # except:
                    #     st.error("PDF File is not readable")
                    
                    # Can comment out 2 line below if using pdfplumber
                    raw_text = read_pdf(doc_file)
                    st.write(raw_text)

                    
                elif doc_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    st.success("Word Document Uploaded")
                    raw_text = docx2txt.process(doc_file)
                    st.write(raw_text)
                    # st.text(raw_text)

    elif choice == "Image":
        st.subheader("Image")
        image_file = st.file_uploader("Drag or Select Images", type=['jpg', 'png', 'jpeg'])
        if st.button("Process"):
            reader = load_model()
            if image_file is not None:  
                img = Image.open(image_file)
                img = np.array(img)

                st.subheader('Image you Uploaded...')
                st.image(image_file,width=450)

                with st.spinner('🤖 AI is extracting text from given Image!'):
                    eng_reader = ocr.Reader(['en'])
                    detected_text = eng_reader.readtext(img)

                st.subheader('Extracted text is ...')
                text = display_text(detected_text)
                st.write(text)

                st.success("Here you go!")
            else:
                st.error("Please upload an image file")
                
                # result = reader.readtext(image_file)
                # st.text(string(result))

                # files_details = {"FileName":image_file.name,"FileType":image_file.type,"FileSize(Byte)":image_file.size} # To get the details of the file
                # st.write(files_details)
                # st.image(image_file, use_column_width=True)
                # st.success("Image Uploaded")
                # raw_text = pytesseract.image_to_data(image_file, output_type=Output.DICT)
                # st.write(raw_text.keys())

    # elif choice == "Image":
    #     st.subheader("Image")
    #     image_file = st.file_uploader("Drag or Select Images", type=['jpg', 'png', 'jpeg'])
    #     if st.button("Process"):
    #         reader = load_model()
    #         if image_file is not None:  
                
    #             reader = ocr.Reader(['en'], model_storage_directory='.', download_enabled=True)
    #             input_image = Image.open(image_file) # read image
    #             st.image(input_image, caption='Input Image', use_column_width=True) # display image

    #             #with st.spinner('Processing...'):
    #             with st.spinner('🤖 AI is at Work! '):

    #                 result = reader.readtext(np.array(input_image))

    #                 result_text = []

    #                 for text in result:
    #                     result_text.append(text[1])
                    
    #                 st.write(result_text)
    #             st.success("Here you go!")
    #         else:
    #             st.error("Please upload an image file")
                
    #             result = reader.readtext(image_file)
    #             st.text(string(result))

    #             files_details = {"FileName":image_file.name,"FileType":image_file.type,"FileSize(Byte)":image_file.size} # To get the details of the file
    #             st.write(files_details)
    #             st.image(image_file, use_column_width=True)
    #             st.success("Image Uploaded")
    #             # raw_text = pytesseract.image_to_data(image_file, output_type=Output.DICT)
    #             # st.write(raw_text.keys())



    
    elif choice == "Dataset":
        st.subheader("Dataset")
        data_file = st.file_uploader("Drag or Select Dataset", type=['csv', 'xlsx', 'txt'])
        if st.button("Process"):
            if data_file is not None:
                # st.write(type(data_file))
                # st.write(dir(data_file))
                files_details = {"FileName":data_file.name,"FileType":data_file.type,"FileSize(Byte)":data_file.size}
                st.write(files_details)
                st.success("Dataset Uploaded")
                df = pd.read_csv(data_file)
                st.dataframe(df)

    elif choice == "TextAnalyzer":
        #st.subheader("Text Analyzer")
        # Creating an object of prediction service
        pred = GeneralModel()

        api_key = st.sidebar.text_input("APIkey", type="password")
        # Using the streamlit cache
        @st.cache
        def process_prompt(input):

            return pred.model_prediction(input=input.strip() , api_key=api_key)

        if api_key:

            # Setting up the Title
            st.subheader("Please insert desired (partial or full) text from your parsed file")

            st.write("---")

            s_example = "The shareholders sold 1,000 shares of common stock of XYZ at $10.00 per share."
            input = st.text_area(
                "An example is provided for your convenience",
                value=s_example,
                max_chars=150,
                height=100,
            )

            if st.button("Submit"):
                with st.spinner(text="In progress"):
                    report_text = process_prompt(input)
                    st.markdown(report_text)
        else:
            st.error("🔑 Please enter API Key")


    elif choice == "About":
        st.subheader("About Audit AI")
        st.text("Audit AI is a tool that allows users to upload documents and images and extract text from them. The text can be then analyzed using the Text Analyzer section.")
        
        st.info("We do not store any data, this tool is built for testing purposes only")
        st.text("Instructions:")
        st.text("1. Select the type of file from the sidebar")
        st.text("2. Upload a document file")
        st.text("3. Click on Process")
        st.text("4. Copy desired text")
        st.text("5. Navigate to Text Analyzer section")
        st.text("6. Input your given API key. If you don't have one, you can use mine: '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'")
        st.text("7. Paste the text into the text area")
        st.text("8. Click on Submit")



        st.text("If you like our product and would like us to create a login key from your team. Contact us at: ")

if __name__ == '__main__':
    main()