import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ Clave OpenAI cargada correctamente desde .env")
else:
    print("❌ No se encontró la clave OPENAI_API_KEY en .env")

pdf_path = "data/documento.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"Total de documentos: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(documents)

print(f"Documento dividido en {len(texts)} fragmentos.")
print(texts[0].page_content[:500])
