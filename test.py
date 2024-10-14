from llama_index.core import SimpleDirectoryReader

# documents = SimpleDirectoryReader(
#     input_files=["./data/paul_graham_essay.txt"]
# ).load_data()


def load_pdf_data(pdf_directory):
    reader = SimpleDirectoryReader(pdf_directory, required_exts=[".pdf"])
    documents = reader.load_data()
    return documents

documents = load_pdf_data("pdfs")

print("Document ID:", documents[0].doc_id)

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
Settings.llm = Ollama(model="llama3")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("LLM ", Settings.llm)
print("EMBEDDING MODEL ", Settings.embed_model)


from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore


vector_store = MilvusVectorStore(uri="./milvus_demo.db", dim=384, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)






query_engine = index.as_query_engine()
while True:
    query = input("Type here ::")
    res = query_engine.query(query)
    print(res)
