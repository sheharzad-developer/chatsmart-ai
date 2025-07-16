import os
import tempfile
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from pdf2image import convert_from_path

# Load Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_pdf(file_input):
    """Load and split PDF into text chunks using PyMuPDF and LangChain splitters."""
    # Check if input is a file path (string) or file object
    if isinstance(file_input, str):
        # If it's a string, assume it's a file path
        pdf_path = file_input
        cleanup_needed = False
    else:
        # If it's a file object (like Streamlit UploadedFile), create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_input.read())
            pdf_path = tmp_file.name
            cleanup_needed = True
    
    try:
        # Load PDF using the file path
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(docs)
        return chunks
    finally:
        # Clean up temporary file only if we created it
        if cleanup_needed and os.path.exists(pdf_path):
            os.unlink(pdf_path)

def create_vectorstore(chunks):
    """Create FAISS vectorstore from document chunks using HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = FAISS.from_documents(chunks, embeddings)
    return vectordb

def load_and_embed(file_obj):
    """Pipeline: Load PDF, split, embed, return retriever."""
    chunks = load_pdf(file_obj)
    vectordb = create_vectorstore(chunks)
    return vectordb.as_retriever()

def get_gemini_response(vectorstore, query):
    """Run LangChain QA chain using Gemini to answer question from vectorstore."""
    retriever = vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(query)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # or "gemini-pro"
        temperature=0.2,
        google_api_key=GOOGLE_API_KEY,
    )

    qa_chain = load_qa_chain(llm, chain_type="stuff")
    response = qa_chain.run(input_documents=docs, question=query)
    return response

def get_pdf_preview(pdf_path):
    """Convert first page of PDF to image for thumbnail preview."""
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    return images[0] if images else None