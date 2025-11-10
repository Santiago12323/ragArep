import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise ValueError("❌ ERROR: Faltan las claves OPENAI_API_KEY o PINECONE_API_KEY en el archivo .env")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "laboratorio-rag1"

try:
    existing_indexes = [index["name"] for index in pc.list_indexes()]
    if index_name not in existing_indexes:
        print(f" Creando índice '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f" Índice '{index_name}' creado correctamente")
    else:
        print(f"ℹEl índice '{index_name}' ya existe, no es necesario crearlo")

except Exception as e:
    print(f" Error al crear o verificar el índice: {e}")


try:
    index = pc.Index(index_name)
    print(f" Conectado al índice: {index_name}")
except Exception as e:
    print(f" No se pudo conectar al índice '{index_name}': {e}")
