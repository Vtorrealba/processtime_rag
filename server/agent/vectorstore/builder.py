import os
from langchain_unstructured import UnstructuredLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Load environment variables
unstructured_api_key = os.getenv("UNSTRUCTURED_API_KEY")


# Load documents
loader = UnstructuredLoader(file_paths, api_key=unstructured_api_key, partition_via_api=True)
docs = loader.load()

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# Create or add to vectorstore
VECTORDB = 'db'
vectorstore = Chroma.from_documents(filter_complex_metadata(splits), embedding=embeddings, persist_directory=VECTORDB)