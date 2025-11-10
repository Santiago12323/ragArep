import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "laboratorio-rag1"

if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise ValueError("❌ ERROR: Faltan claves en el archivo .env")


client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(INDEX_NAME)
print(f" Conectado al índice '{INDEX_NAME}'")


pdf_path = "data/documento.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f" No se encontró el archivo: {pdf_path}")

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f" Total de páginas: {len(documents)}")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(documents)
print(f" Documento dividido en {len(docs)} fragmentos")


for i, doc in enumerate(docs):
    texto = doc.page_content.strip()
    if not texto:
        continue

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto
    ).data[0].embedding

    index.upsert([
        {
            "id": str(uuid4()),
            "values": embedding,
            "metadata": {"texto": texto}
        }
    ])

    print(f" Fragmento {i+1}/{len(docs)} subido")

print("\n Todos los fragmentos del PDF fueron subidos exitosamente a Pinecone.")
