from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
import streamlit as st
import hashlib


def load_pdf_data(pdf_directory):
    reader = SimpleDirectoryReader(pdf_directory, required_exts=[".pdf"])
    documents = reader.load_data()
    return documents

def load_pdf_files(input_files):
    reader = SimpleDirectoryReader(input_files=input_files, required_exts=[".pdf"])
    documents = reader.load_data()
    return documents


Settings.llm = Ollama(model="llama3")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("LLM ", Settings.llm)
print("EMBEDDING MODEL ", Settings.embed_model)


def get_engine(documents):
    vector_store = MilvusVectorStore(uri="./milvus_demo.db", dim=384, overwrite=True)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
    return query_engine


st.title("Llamaindex PDF Chatbot using Milvs and Ollama")

# Sidebar for PDF Upload
st.sidebar.header("Upload PDF")
uploaded_pdf = st.sidebar.file_uploader("Choose a PDF file", type="pdf",accept_multiple_files=True)
submit_button = st.sidebar.button("Submit")



if "documents" not in st.session_state:
    st.session_state.documents = None

if "engine" not in st.session_state:
    st.session_state.engine = None

if submit_button and uploaded_pdf is not None:
    print("@@@@@@@@",uploaded_pdf)
    files = []
    for file in uploaded_pdf:
        file_hash = hashlib.md5(file.getvalue()).hexdigest()
        filename = f"temp_{file_hash}.pdf"
        files.append(filename)
        with open(filename, "wb") as f:
            f.write(file.getbuffer())
    st.documents = load_pdf_files(files)
    st.engine = get_engine(st.documents)



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    print("USER :: ", prompt)
    with st.chat_message("assistant"):
        stream = st.engine.query(prompt)
        response = st.write_stream(stream.response_gen)
    st.session_state.messages.append({"role": "assistant", "content": response})