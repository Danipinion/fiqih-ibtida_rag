# 🤖 RAG Fiqih Ibtida — UTS Data Engineering

> **Retrieval-Augmented Generation** — Sistem Tanya-Jawab Cerdas Berbasis Dokumen Kitab Fiqih Dasar (Fathul Qorib, Kasyifatus Saja, Safinatun Najah).

Proyek ini adalah implementasi sistem RAG (Retrieval-Augmented Generation) yang dirancang untuk membantu pengguna memahami hukum-hukum fiqih berdasarkan sumber kitab klasik yang telah dikonversi menjadi data digital.

---

## 👥 Identitas Kelompok

| Nama                          | NIM       | Tugas Utama     |
| ---------------------------- | --------- | --------------- |
| Mohammad Dani Taufiqurrohman | 244311048 | Data Engineer   |
| Habib Hajid Taqiudin         | 244311043 | Project Manager |
| Novandy Triarto Wahyono      | 244311053 | Data Analyst    |

**Topik Domain:** *Akademik & Keagamaan (Fiqih)* 
**Stack Teknis:** *Python (From Scratch)* 
**LLM:** *Gemini 2.5 Flash* 
**Vector DB:** *ChromaDB* 
**Embedding:** *Google Generative AI Embeddings*

---

## 🗂️ Struktur Proyek

```text
fiqih-ibtida_rag/
├── data/                    # Dokumen sumber
│   ├── Feqih trendy.pdf
│   ├── Fiqih Idola Terjemah Fathul Qorib - 1.pdf
│   ├── SafinatunNajah-syaikhSalimBinSumair.docx
│   └── Terjemah-Kasyifatus-Saja-1.pdf
├── src/
│   ├── embeddings.py        # Konfigurasi model embedding
│   ├── indexing.py          # Pipeline pemrosesan dokumen ke Vector DB
│   ├── query.py             # Logika retrieval dan augmentasi ke Gemini
│   └── __init__.py
├── ui/
│   └── app.py               # Interface Streamlit
├── evaluation/
│   └── template_evaluasi.csv # Data uji performa sistem
├── .env                     # Konfigurasi
├── requirements.txt         # Daftar library Python
└── README.md
```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone [https://github.com/danipinion/fiqih-ibtida_rag.git](https://github.com/danipinion/fiqih-ibtida_rag.git)
cd fiqih-ibtida_rag

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

### 4. Jalankan Indexing

```bash
python src/indexing.py
```

### 5. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run ui/app.py
```

---

## 🔧 Konfigurasi

Semua konfigurasi utama ada di `src/config.py` (atau langsung di setiap file):

| Parameter       | Default | Keterangan                          |
| --------------- | ------- | ----------------------------------- |
| `CHUNK_SIZE`    | 500     | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 50      | Overlap antar chunk                 |
| `TOP_K`         | 3       | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME`    | _gemini-2.5-flash_ | Mesin AI untuk pemrosesan jawaban       |

---

## 📊 Hasil Evaluasi

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

- Framework: _Scract_
- LLM: _Gemini_
- Vector DB: _ChromaDB_

---

## 👨‍🏫 Informasi UTS

- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
