import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "laboratorio-rag1"

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

print("Chat con tu documento PDF (escribe 'salir' para terminar)\n")

while True:
    query = input("Tú: ").strip()
    if query.lower() in ["salir", "exit", "quit"]:
        print("Fin del chat.")
        break

    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )

    context = "\n".join([m['metadata']['texto'] for m in results['matches']])

    prompt = f"""
Responde basándote solo en la siguiente información:

{context}

Pregunta: {query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    print(f"\nAsistente: {answer}\n")
