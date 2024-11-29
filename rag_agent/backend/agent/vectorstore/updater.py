import os
from langchain_unstructured import UnstructuredLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata


# Función para agregar documentos al vectorstore
def add_document_to_vectorstore(file, vectordb_path = 'db'):
    try:
        # Guardar el archivo en el directorio de documentos para mantener un registro
        documents_dir = "documents"
        file_path = os.path.join(documents_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # Cargar el documento usando UnstructuredLoader
        unstructured_api_key = os.getenv("UNSTRUCTURED_API_KEY")
        loader = UnstructuredLoader([file_path], api_key=unstructured_api_key, partition_via_api=True)
        docs = loader.load()

        # Inicializar embeddings
        embeddings = OpenAIEmbeddings()

        # Dividir los documentos en fragmentos
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        # Cargar la base de datos existente y agregar los nuevos documentos
        vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embeddings)
        vectordb.add_documents(filter_complex_metadata(splits))

        return True  # Operación exitosa
    except Exception as e:
        print(f"Error al añadir el documento: {e}")
        return False