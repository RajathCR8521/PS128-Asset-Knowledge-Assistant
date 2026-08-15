# 🤖 Asset Knowledge Assistant

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**. Upload any PDF document and ask natural language questions to receive context-aware answers generated using Google Gemini.

---

## ✨ Features

- 📄 Upload any PDF document
- 🔍 Extract and process document text
- 🧠 Generate semantic embeddings using Sentence Transformers
- ⚡ Store embeddings in a FAISS vector database
- 🤖 Retrieve relevant document chunks using RAG
- 💬 Generate answers using Google Gemini
- 🌐 Simple and interactive Streamlit interface

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| LLM | Google Gemini |
| PDF Processing | PyPDF2 |

---

## 📸 Screenshots

### Home Page

![Home](docs/home.png)

---

### Upload PDF

![Upload](docs/upload.png)

---

### Generated Answer

![Answer](docs/answer.png)

---

## 📂 Project Structure

```
PS128-Asset-Knowledge-Assistant/
│
├── backend/
│   ├── embedder.py
│   ├── llm.py
│   ├── pdf_reader.py
│   ├── rag.py
│   └── vector_store.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── home.png
│   ├── upload.png
│   └── answer.png
│
├── scripts/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/RajathCR8521/PS128-Asset-Knowledge-Assistant.git
```

Go to the project directory

```bash
cd PS128-Asset-Knowledge-Assistant
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run frontend/app.py
```

---

## 🚀 Future Improvements

- Multiple PDF support
- Chat history
- Source citation
- Hybrid Search (BM25 + FAISS)
- OCR support for scanned PDFs
- Docker deployment
- Cloud deployment

---

## 👨‍💻 Author

**Rajath CR**

B.Tech Computer Science & Engineering (Cybersecurity)

Dayananda Sagar University

---

## 📄 License

This project is licensed under the MIT License.