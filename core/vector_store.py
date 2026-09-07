import os 
from langchain_chroma import Chroma 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,model_kwargs={"device": 'cpu'})


def build_vector_store(text:str)->Chroma:

    embeddings = get_embeddings()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

    docs = [Document(page_content=chunk, metadata={"source": "meeting_transcript"}) 
        for chunk in splitter.split_text(text)
    ]


    vector_store = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        collection_name=COLLECTION_NAME, 
        persist_directory=CHROMA_DIR
    )
    return vector_store


def load_vector_store()->Chroma:
    embeddings = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding=embeddings, 
        persist_directory=CHROMA_DIR
    )

def get_retriever(vector_store:Chroma, k:int=4)->Chroma:
    
    return vector_store.as_retriever(search_kwargs={"k": k})
