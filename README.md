# FinBase RAG Assistant 💳🤖

An AI-powered FinTech Customer Support Assistant that answers financial questions using information retrieved from a knowledge base of financial PDF documents.

## 🚀 Live Demo

**Try the application here:**  
https://finbase-rag-assistant-hwp5yn7vzcrujpycntsq3a.streamlit.app/

## 📌 Project Overview

FinBase RAG Assistant uses Retrieval-Augmented Generation (RAG) to provide context-aware answers to financial customer support questions. Instead of relying only on the language model's general knowledge, it retrieves relevant passages from financial documents and uses them to generate responses.

## ✨ Key Features

- **PDF-based knowledge base:** Extracts text from financial PDF documents.
- **Text chunking:** Splits documents into smaller, overlapping chunks for retrieval.
- **Semantic embeddings:** Uses `BAAI/bge-small-en-v1.5` to represent text and questions as vectors.
- **Vector similarity search:** Uses FAISS to retrieve relevant document chunks.
- **AI-powered responses:** Uses Google Gemini (`gemini-2.5-flash`) to generate answers from retrieved context.
- **Source references:** Displays retrieved source documents and page information.
- **Interactive interface:** Provides a chat-based interface built with Streamlit.

## 🏗️ Architecture

1. **Document ingestion:** Extract text from financial PDFs using PyMuPDF.
2. **Chunking:** Split the extracted text using LangChain's `RecursiveCharacterTextSplitter`.
3. **Embedding generation:** Generate normalized embeddings using Sentence Transformers.
4. **Vector indexing:** Store embeddings in a FAISS index.
5. **Retrieval:** Find relevant chunks using vector similarity search.
6. **Answer generation:** Pass the retrieved context and user question to Google Gemini.
7. **User interface:** Display the answer and source references in Streamlit.

## 🛠️ Tech Stack

- **Language:** Python
- **LLM:** Google Gemini 2.5 Flash
- **Embeddings:** Sentence Transformers — BAAI/bge-small-en-v1.5
- **Vector database/index:** FAISS
- **Document processing:** PyMuPDF
- **Frameworks:** LangChain, Streamlit
- **Environment management:** python-dotenv

## 📂 Project Structure

```text
finbase-rag-assistant/
├── data/
│   └── raw/
├── evaluation/
│   ├── eval.py
│   └── eval_ques.json
├── src/
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── retriever.py
│   ├── llm.py
│   ├── rag.py
│   └── streamlit_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/manishaparihar714/finbase-rag-assistant.git
cd finbase-rag-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never commit your actual API key to GitHub.

### 5. Build the vector store

If the vector store is not already included in the repository, place the authorized financial PDF documents in `data/raw/` and run:

```bash
python -m src.vectorstore
```

### 6. Launch the application

```bash
streamlit run src/streamlit_app.py
```

## 🔐 Security

- API keys are stored in environment variables or Streamlit secrets.
- The `.env` file should not be committed to version control.
- Only authorized documents should be included in the public repository.

## 📈 Future Improvements

- Expand the financial knowledge base.
- Improve retrieval quality and relevance ranking.
- Add automated evaluation of answer quality and retrieval performance.
- Add conversation history and enhanced error handling.
- Explore hybrid search and reranking for more accurate retrieval.

## 👩‍💻 Author

**Manisha Parihar**

B.Tech — Data Science

[GitHub Profile](https://github.com/manishaparihar714)

---

*Built as an AI-powered FinTech customer support project using Retrieval-Augmented Generation.*
