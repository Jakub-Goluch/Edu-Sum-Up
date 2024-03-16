from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import CharacterTextSplitter


def get_documents_txt(path):
    loader = TextLoader(path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


def get_documents_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    return text_splitter.split_documents(pages)
