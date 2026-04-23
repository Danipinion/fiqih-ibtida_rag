import os
import chromadb
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
from src.embeddings import get_chroma_embedding_function

# Load configuration
load_dotenv()

VS_DIR        = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))
TOP_K         = int(os.getenv("TOP_K", 3))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL     = os.getenv("LLM_MODEL_NAME", "gemini-1.5-flash")

# Configure Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def get_collection():
    """
    Connects to the ChromaDB collection.
    """
    if not VS_DIR.exists():
        raise FileNotFoundError(f"Vector store not found at {VS_DIR}. Run indexing.py first.")
    
    client = chromadb.PersistentClient(path=str(VS_DIR))
    emb_fn = get_chroma_embedding_function()
    
    return client.get_collection(name="rag_collection", embedding_function=emb_fn)

def retrieve_context(collection, question: str, top_k: int = TOP_K):
    """
    Search for relevant context in ChromaDB.
    """
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    
    contexts = []
    # results format is a bit nested in chromadb
    for i in range(len(results['documents'][0])):
        contexts.append({
            "content": results['documents'][0][i],
            "source": results['metadatas'][0][i].get("source", "unknown"),
            "distance": results['distances'][0][i] if 'distances' in results else None
        })
    
    return contexts

def build_prompt(question: str, contexts: list):
    """
    Construct the prompt for Gemini.
    """
    context_text = "\n\n---\n\n".join(
        [f"[Sumber: {c['source']}]\n{c['content']}" for c in contexts]
    )

    prompt = f"""Kamu adalah asisten akademik yang membantu menjawab pertanyaan berdasarkan dokumen yang diberikan.

INSTRUKSI:
- Jawab HANYA berdasarkan konteks di bawah ini.
- Jika jawaban tidak ada dalam konteks, katakan "Maaf, saya tidak menemukan informasi tersebut dalam dokumen akademik yang tersedia."
- Jawab dalam Bahasa Indonesia yang formal, jelas, dan ringkas.
- Jangan mengarang informasi di luar konteks.

KONTEKS:
{context_text}

PERTANYAAN:
{question}

JAWABAN:"""
    
    return prompt

def get_answer_gemini(prompt: str):
    """
    Generate answer using Google Gemini API.
    """
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY tidak ditemukan di .env"
    
    try:
        model = genai.GenerativeModel(LLM_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error saat memanggil Gemini API: {e}"

def answer_question(question: str, collection=None):
    """
    Complete RAG pipeline: retrieval -> prompt -> generation.
    """
    if collection is None:
        collection = get_collection()
    
    # 1. Retrieval
    contexts = retrieve_context(collection, question)
    
    # 2. Build Prompt
    prompt = build_prompt(question, contexts)
    
    # 3. Generation
    answer = get_answer_gemini(prompt)
    
    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "prompt": prompt
    }

if __name__ == "__main__":
    print("-" * 30)
    print("🤖 RAG CLI - GEMINI + CHROMADB")
    print("-" * 30)
    
    try:
        coll = get_collection()
        print("✅ Vector database loaded.")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

    while True:
        query = input("\n❓ Tanya sesuatu (atau 'q' untuk keluar): ")
        if query.lower() == 'q':
            break
        
        result = answer_question(query, coll)
        print("\n🤖 JAWABAN:")
        print(result["answer"])
        print("\n📚 KONTEKS RELEVAN:")
        for i, ctx in enumerate(result["contexts"], 1):
            print(f"   [{i}] {ctx['source']} (Score: {ctx.get('distance', 'N/A')})")
