# ⚡ PS128 Asset Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based knowledge assistant designed for **energy and utilities technical documentation**.

The system allows users to ask natural-language questions about transformer equipment, transformer protection, maintenance, operation, and related technical information.

Instead of manually searching through multiple technical documents, the assistant retrieves relevant document content using semantic search and uses **Google Gemini** to generate a grounded answer.

---

## 🎯 Problem Statement

Energy and utility assets such as transformers involve large amounts of technical documentation, including manuals, datasheets, protection documentation, maintenance information, and equipment specifications.

Finding specific information manually across multiple documents can be time-consuming.

The **PS128 Asset Knowledge Assistant** addresses this problem by providing a natural-language interface over a technical document knowledge base.

A user can ask a technical question, and the system:

1. Understands the question.
2. Searches the technical knowledge base.
3. Retrieves the most relevant document sections.
4. Provides the retrieved information to Google Gemini.
5. Generates a grounded response.
6. Displays the source documents used for the response.

---

# 💡 Solution

The project implements a **Retrieval-Augmented Generation (RAG)** pipeline.

### Overall Architecture

```text
                 TECHNICAL DOCUMENTS
                         │
                         ▼
                ┌─────────────────┐
                │  PDF Extraction │
                │    PyMuPDF      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Chunking   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Sentence        │
                │ Transformers    │
                │ Embeddings      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ FAISS Vector    │
                │ Index           │
                └────────┬────────┘
                         │
                         │
              ┌──────────▼──────────┐
              │    User Question    │
              └──────────┬──────────┘
                         │
                         ▼
                Question Embedding
                         │
                         ▼
                Semantic Retrieval
                         │
                         ▼
                Relevant Chunks
                         │
                         ▼
                ┌─────────────────┐
                │  Google Gemini  │
                │      LLM        │
                └────────┬────────┘
                         │
                         ▼
                Grounded Answer
                         │
                         ▼
                 Source Documents
```

---

# 🏗️ System Architecture

The application is divided into three major layers.

## 1. Document Processing Layer

Technical PDF documents are stored locally in the project's knowledge-base directory.

**PyMuPDF** is used to extract text from each PDF.

The extracted content is then divided into smaller chunks so that individual relevant sections can be retrieved instead of processing an entire document for every question.

---

## 2. Retrieval Layer

The project uses **Sentence Transformers** to convert document chunks into numerical vector representations called embeddings.

The embedding model used is:

```text
all-MiniLM-L6-v2
```

The model produces:

```text
384-dimensional embeddings
```

The embeddings are stored and searched using **FAISS**.

When the user asks a question:

```text
Question
   ↓
Question Embedding
   ↓
FAISS Similarity Search
   ↓
Relevant Document Chunks
```

The retrieved chunks are then passed to the generation layer.

---

## 3. Generation Layer

The retrieved technical information is provided as context to **Google Gemini**.

Gemini generates the final answer based on the retrieved context.

The system is designed to avoid fabricating technical information when the requested information is not available in the knowledge base.

The application also identifies the source documents associated with the retrieved information.

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend REST API |
| Streamlit | Frontend web interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Semantic embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector similarity search |
| Google Gemini | Answer generation |
| NumPy | Numerical operations |
| Pydantic | API request validation |
| Uvicorn | FastAPI application server |

---

# 📂 Project Structure

```text
PS128-Asset-Knowledge-Assistant/
│
├── backend/
│   ├── embedder.py
│   ├── llm.py
│   ├── main.py
│   ├── pdf_reader.py
│   ├── rag.py
│   └── vector_store.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── Technical PDF documents
│   │
│   └── processed/
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Backend

| File | Responsibility |
|---|---|
| `pdf_reader.py` | Extracts text from PDF documents |
| `embedder.py` | Generates document and query embeddings |
| `vector_store.py` | Creates and searches the FAISS index |
| `llm.py` | Communicates with Google Gemini |
| `rag.py` | Coordinates the complete RAG pipeline |
| `main.py` | Provides the FastAPI backend and API endpoints |

### Frontend

`frontend/app.py` provides the Streamlit user interface for interacting with the assistant.

---

# 📚 Knowledge Base

The current local knowledge base contains **four technical documents** focused on transformer equipment and protection.

The documents cover areas including:

- Transformer installation
- Transformer commissioning
- Transformer operation
- Transformer maintenance
- Transformer accessories
- Transformer troubleshooting
- Transformer oil-related information
- Transformer protection
- SEL-787 transformer protection relay
- Protection functions
- Technical specifications

The source PDFs are intentionally **not included in the public GitHub repository**.

They are maintained locally inside:

```text
data/raw/
```

---

# 🔄 RAG Pipeline

## Step 1 — PDF Extraction

The system uses **PyMuPDF** to open the technical PDF documents and extract text page by page.

The extracted text is combined into a document-level text representation.

---

## Step 2 — Text Chunking

The extracted document text is divided into smaller chunks.

The current implementation uses approximately:

```text
500 characters per chunk
```

Chunking allows the retrieval system to work with smaller sections of technical documentation.

---

## Step 3 — Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The resulting vectors have:

```text
384 dimensions
```

The embeddings are converted to NumPy `float32` arrays before being passed to FAISS.

---

## Step 4 — FAISS Indexing

The generated embeddings are stored in a FAISS vector index.

FAISS enables similarity-based searching across the document embeddings.

Conceptually:

```text
Document Chunk
      ↓
Embedding Vector
      ↓
FAISS Index
```

---

## Step 5 — Question Embedding

When a user asks a question, the same embedding model converts the question into a 384-dimensional vector.

```text
User Question
      ↓
Sentence Transformer
      ↓
Question Embedding
```

---

## Step 6 — Semantic Retrieval

The question embedding is compared against the document embeddings stored in FAISS.

The most relevant chunks are retrieved.

```text
Question
   ↓
Embedding
   ↓
FAISS Search
   ↓
Relevant Chunks
```

This allows the system to retrieve information based on **semantic similarity**, rather than requiring the user to use the exact wording present in the documents.

---

## Step 7 — Context Construction

The retrieved chunks are combined into a context for the language model.

The context contains technical information retrieved from the knowledge base along with source-document information.

---

## Step 8 — Gemini Generation

Google Gemini receives:

- The user's question
- Retrieved technical context
- Instructions for generating a grounded response

The model then generates the final answer.

---

## Step 9 — Source Attribution

The retrieved chunks retain their associated source-document information.

The application can therefore identify the technical documents that contributed to the answer.

---

# 🔐 Knowledge Grounding

A key objective of the system is to reduce unsupported or fabricated responses.

The generation process instructs the model to:

1. Use retrieved technical documentation as the primary source.
2. Avoid inventing technical information.
3. Answer using the available context.
4. Clearly indicate when requested information is not available.
5. Provide technically relevant responses.
6. Identify relevant source documents.

For example, the system was tested with a question about the failure history of a transformer asset that was not present in the knowledge base.

Instead of generating a fictional failure history, the assistant indicated that the requested information was not available in the retrieved knowledge base.

---

# 🖥️ Application

The project contains two application components:

```text
┌───────────────────────┐
│   Streamlit Frontend  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    FastAPI Backend    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      RAG Pipeline     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Technical Knowledge   │
│       Base            │
└───────────────────────┘
```

### Streamlit Frontend

The Streamlit interface provides:

- Backend status
- Knowledge-base initialization
- Question input
- Generated answers
- Retrieved source documents
- Interactive interaction with the assistant

### FastAPI Backend

The FastAPI application handles:

- API requests
- RAG initialization
- Question processing
- Answer generation
- Error handling

---

# 🔌 API Endpoints

## Root

```http
GET /
```

Returns a basic API status message.

---

## Health Check

```http
GET /health
```

Used to verify that the backend is running.

Example:

```json
{
  "status": "healthy"
}
```

---

## Initialize Knowledge Base

```http
POST /initialize
```

Initializes the RAG pipeline by:

1. Reading the technical PDFs.
2. Extracting their text.
3. Creating chunks.
4. Generating embeddings.
5. Building the FAISS index.

---

## Ask a Question

```http
POST /ask
```

Example request:

```json
{
  "question": "What protection functions are provided by the SEL-787 transformer protection relay?"
}
```

The backend processes the question through the RAG pipeline and returns the generated response.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/RajathCR8521/PS128-Asset-Knowledge-Assistant.git
```

Move into the project:

```bash
cd PS128-Asset-Knowledge-Assistant
```

---

## 2. Create a Virtual Environment

On Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

The `.env` file is excluded from Git using `.gitignore`.

**Never commit API keys or other secrets to GitHub.**

---

# 📄 Add Technical Documents

Place the required technical PDF documents inside:

```text
data/raw/
```

The project uses these documents as the local knowledge base.

The PDF files are excluded from the public GitHub repository.

---

# ▶️ Running the Application

The backend and frontend run separately.

## Start FastAPI

From the project root:

```bash
uvicorn backend.main:app --reload
```

The backend normally runs at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The frontend normally runs at:

```text
http://localhost:8501
```

---

# 🧪 Example Questions

The system has been tested with questions including:

### Transformer Maintenance

```text
What maintenance activities are recommended for transformers?
```

### Transformer Oil

```text
What information is available in the knowledge base about transformer oil?
```

### Transformer Protection

```text
What protection functions are provided by the SEL-787 transformer protection relay?
```

### Cross-Document Question

```text
What information is available about transformer oil and what protection functions are provided by the SEL-787 relay?
```

### Missing Information

```text
What is the failure history of transformer TX-101?
```

For information that is not present in the knowledge base, the system is designed to indicate that the information is unavailable rather than fabricate a response.

---

# 📊 Current Implementation

The current knowledge-base implementation was tested using:

```text
Documents: 7
Chunks: 1330
Embedding Dimension: 384
Embedding Model: all-MiniLM-L6-v2
Vector Search: FAISS
LLM: Google Gemini
```

The system was tested across:

- Transformer maintenance questions
- Transformer oil questions
- Transformer protection questions
- SEL-787 protection questions
- Cross-document questions
- Missing-information questions
- Source-document retrieval

---

# 🧪 Validation

The RAG pipeline was manually tested through the application and FastAPI interface.

### Test 1 — Transformer Protection

The assistant successfully retrieved protection-related information from the SEL-787 technical documents.

### Test 2 — Transformer Oil

The assistant successfully retrieved available transformer-oil-related information from the transformer documentation.

### Test 3 — Cross-Document Retrieval

The system was able to retrieve information from different technical documents for a combined question.

### Test 4 — Missing Information

The system was asked for failure history for an asset that was not represented in the knowledge base.

The assistant correctly indicated that the information was not available rather than generating unsupported information.

---

# 🔒 Security and Repository Practices

The repository intentionally excludes:

- `.env` files
- API keys
- Virtual environments
- Python cache files
- Generated vector data
- Temporary files
- Third-party technical PDFs

The source documents remain local and are not redistributed through the GitHub repository.

---

# 🔮 Future Improvements

Possible future improvements include:

- Page-level source citations
- Improved chunking with overlap
- Hybrid keyword + semantic retrieval
- Metadata-based filtering
- Asset-specific metadata
- Transformer and substation asset records
- Historical failure records
- Maintenance history
- Technical drawing and schematic retrieval
- Document upload through the frontend
- Persistent vector database
- Retrieval evaluation metrics
- Automated response evaluation
- Authentication and access control
- Docker deployment
- Cloud deployment

These are future extensions and are not presented as existing functionality.

---

# 🎓 Project Objective

The objective of the **PS128 Asset Knowledge Assistant** is to demonstrate how Retrieval-Augmented Generation can be applied to technical knowledge management in the **energy and utilities domain**.

The project combines:

```text
Technical Documentation
        +
Semantic Retrieval
        +
Vector Search
        +
Generative AI
```

to provide a natural-language interface for interacting with technical asset documentation.

---

# 👨‍💻 Author

**Rajath CR**

B.Tech Computer Science & Engineering  
Specialization: Cybersecurity  
Dayananda Sagar University

---

# 📄 License

This repository contains the application source code.

Third-party technical documents used during development are not redistributed through this repository.