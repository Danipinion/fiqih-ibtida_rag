import os
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from pypdf import PdfReader
from docx import Document
from src.embeddings import get_chroma_embedding_function

# Load configuration
load_dotenv()

CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
DATA_DIR      = Path(os.getenv("DATA_DIR", "./data"))
VS_DIR        = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))

def load_documents(data_dir: Path):
    """
    Load TXT and PDF documents from the data directory.
    """
    documents = []

    # Load PDF files
    for file_path in data_dir.glob("**/*.pdf"):
        try:
            reader = PdfReader(file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
            documents.append({"content": content, "metadata": {"source": file_path.name}})
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    # Load DOCX files
    for file_path in data_dir.glob("**/*.docx"):
        try:
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            documents.append({"content": content, "metadata": {"source": file_path.name}})
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return documents

def split_text(documents, chunk_size, chunk_overlap):
    """
    Split documents into smaller chunks.
    """
    chunks = []
    for doc in documents:
        text = doc["content"]
        metadata = doc["metadata"]
        
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({
                "content": chunk,
                "metadata": metadata
            })
            start += chunk_size - chunk_overlap
            
    return chunks

def build_index():
    print("=" * 50)
    print("🚀 Memulai Pipeline Indexing (ChromaDB)")
    print("=" * 50)

    # 1. Load Documents
    print("\n📄 Langkah 1: Memuat dokumen...")
    raw_docs = load_documents(DATA_DIR)
    print(f"   {len(raw_docs)} dokumen ditemukan.")

    # 2. Split Text
    print(f"\n✂️  Langkah 2: Memecah dokumen (chunk_size={CHUNK_SIZE})...")
    chunks = split_text(raw_docs, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"   {len(chunks)} chunk dibuat.")

    # 3. Setup ChromaDB and Add Documents
    print(f"\n📦 Langkah 3: Menyimpan ke ChromaDB ({VS_DIR})...")
    
    # Initialize Chroma client
    client = chromadb.PersistentClient(path=str(VS_DIR))
    
    # Get embedding function
    emb_fn = get_chroma_embedding_function()
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="rag_collection",
        embedding_function=emb_fn
    )

    ids = [f"id_{i}" for i in range(len(chunks))]
    documents = [c["content"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    # Add in batches to avoid any size limits
    batch_size = 100
    for i in tqdm(range(0, len(ids), batch_size), desc="Indexing"):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )

    print("\n" + "=" * 50)
    print("✅ Indexing selesai!")
    print("=" * 50)

if __name__ == "__main__":
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        print(f"Folder {DATA_DIR} dibuat. Silakan masukkan dokumen di sana.")
    else:
        build_index()
