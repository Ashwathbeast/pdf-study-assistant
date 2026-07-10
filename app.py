import streamlit as st
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
st.title("PDF Study Assistant")
st.write("Upload a PDF and ask questions about it")
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
question = st.text_input("Ask a question about your PDF")
if st.button("Get Answer"):
    if uploaded_file is None:
        st.error("Please upload a PDF first")
    elif question == "":
        st.error("Please type a question")
    else:
        reader = PdfReader(uploaded_file)
        if len(reader.pages) > 1000:
            st.warning("Large PDF detected. Reading first 1000 pages only.")
            pages_to_read = reader.pages[:1000]
        else:
            pages_to_read = reader.pages
        pdf_text = ""
        for page in pages_to_read:
            pdf_text += page.extract_text()
        prompt = f"""
        Here is a document:
        {pdf_text}
        
        Answer this question based only on the document:
        {question}
        """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    st.subheader("Answer:")
    st.write(response.text)
if st.button("Generate Practice Questions"):
    prompt = f"""
    Based on this document:
    {pdf_text}
    
    Generate 10 multiple choice questions to test understanding.
    Format each question as:
    Q1. Question here
    a) Option 1
    b) Option 2
    c) Option 3
    d) Option 4
    Answer: correct option
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    st.subheader("Practice Questions:")
    st.write(response.text)