# 🤖 RAG Starter Pack — UTS Data Engineering

> **Retrieval-Augmented Generation** — Sistem Tanya-Jawab Cerdas Berbasis Dokumen

Starter pack ini adalah **kerangka awal** proyek RAG untuk UTS Data Engineering D4.
Mahasiswa mengisi, memodifikasi, dan mengembangkan kode ini sesuai topik kelompok masing-masing.

---

## 👥 Identitas Kelompok

| Nama                         | NIM       | Tugas Utama     |
| ---------------------------- | --------- | --------------- |
| Mohammad Dani Taufiqurrohman | 244311048 | Data Engginer   |
| Habib Hajid Taqiudin         | 244311043 | Project Manager |
| Novandy Triarto Wahyono      | 244311053 | Data Analyst    |

**Topik Domain:** _Akademik_
**Stack yang Dipilih:** _From Scratch_  
**LLM yang Digunakan:** _Gemini_
**Vector DB yang Digunakan:** _ChromaDB_

---

## 🗂️ Struktur Proyek

```
rag-uts-[nama-kelompok]/
├── data/                    # Dokumen sumber Anda (PDF, TXT, dll.)
│   └── sample.txt           # Contoh dokumen (ganti dengan dokumen Anda)
├── src/
│   ├── indexing.py          # 🔧 WAJIB DIISI: Pipeline indexing
│   ├── query.py             # 🔧 WAJIB DIISI: Pipeline query & retrieval
│   ├── embeddings.py        # 🔧 WAJIB DIISI: Konfigurasi embedding
│   └── utils.py             # Helper functions
├── ui/
│   └── app.py               # 🔧 WAJIB DIISI: Antarmuka Streamlit
├── docs/
│   └── arsitektur.png       # 📌 Diagram arsitektur (buat sendiri)
├── evaluation/
│   └── hasil_evaluasi.xlsx  # 📌 Tabel evaluasi 10 pertanyaan
├── notebooks/
│   └── 01_demo_rag.ipynb    # Notebook demo dari hands-on session
├── .env.example             # Template environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone https://github.com/[username]/rag-uts-[kelompok].git
cd rag-uts-[kelompok]

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# atau: venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi API Key

```bash
# Salin template env
cp .env.example .env

# Edit .env dan isi API key Anda
# JANGAN commit file .env ke GitHub!
```

### 3. Siapkan Dokumen

Letakkan dokumen sumber Anda di folder `data/`:

```bash
# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/
```

### 4. Jalankan Indexing (sekali saja)

```bash
python src/indexing.py
```

### 5. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run ui/app.py

# Atau via CLI
python src/query.py
```

---

## 🔧 Konfigurasi

Semua konfigurasi utama ada di `src/config.py` (atau langsung di setiap file):

| Parameter       | Default | Keterangan                          |
| --------------- | ------- | ----------------------------------- |
| `CHUNK_SIZE`    | 500     | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 50      | Overlap antar chunk                 |
| `TOP_K`         | 3       | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME`    | _(isi)_ | Nama model LLM yang digunakan       |

---

## 📊 Hasil Evaluasi

_(Isi setelah pengujian selesai)_

| #   | Pertanyaan | Jawaban Sistem | Jawaban Ideal | Skor (1-5) |
| --- | ---------- | -------------- | ------------- | ---------- |
| 1   | ...        | ...            | ...           | ...        |
| 2   | ...        | ...            | ...           | ...        |

**Rata-rata Skor:** ...  
**Analisis:** ...

---

## 🏗️ Arsitektur Sistem

_(Masukkan gambar diagram arsitektur di sini)_

```
[Dokumen] → [Loader] → [Splitter] → [Embedding] → [Vector DB]
                                                         ↕
[User Query] → [Query Embed] → [Retriever] → [Prompt] → [LLM] → [Jawaban]
```

---

## 📚 Referensi & Sumber

- Framework: _(LangChain docs / LlamaIndex docs)_
- LLM: _(Groq / Gemini / Ollama)_
- Vector DB: _(ChromaDB / FAISS docs)_
- Tutorial yang digunakan: _(cantumkan URL)_

---

## 👨‍🏫 Informasi UTS

- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
- **Deadline:** _(isi tanggal)_
