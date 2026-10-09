# FinBase RAG Assistant

An AI-powered financial document assistant that uses Retrieval-Augmented Generation (RAG) to answer questions about financial PDFs using relevant document context.

> **Project status:** In development. Update this README as features are completed and tested.

## Features

- Extract text from PDF documents.
- Split document text into overlapping chunks while preserving source and page metadata.
- Generate semantic embeddings with `BAAI/bge-small-en-v1.5`.
- Search for relevant document chunks using FAISS.
- Generate context-aware answers using a Gemini model.
- Provide a Streamlit interface for interacting with the assistant.
- Evaluate answer quality using a set of evaluation questions.

Some features may require integration or testing before they are fully usable.

## Tech Stack

- **Language:** Python
- **UI:** Streamlit
- **PDF extraction:** PyMuPDF
- **Text splitting:** LangChain text splitters
- **Embeddings:** Sentence Transformers (BGE small English v1.5)
- **Vector search:** FAISS
- **LLM:** Google Gemini
- **Evaluation:** Python

## Project Structure

```text
finbase-rag-assistant/
├── app/                    # Optional application UI folder, if used
├── data/
│   └── raw/                 # Local PDF documents (ignored by Git)
├── evaluation/
│   ├── eval.py              # Evaluation script
│   └── eval_ques.json       # Evaluation questions
├── src/
│   ├── ingestion.py         # Extract PDF text and metadata
│   ├── chunking.py          # Split extracted text into chunks
│   ├── embeddings.py        # Create vector embeddings
│   ├── vectorstore.py       # Build/manage the vector index
│   ├── retriever.py         # Retrieve relevant chunks
│   ├── llm.py               # Configure the language model
│   ├── rag.py               # Connect retrieval and generation
│   └── streamlit_app.py     # Streamlit user interface
├── .env.example             # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- Git
- A Google Gemini API key for Gemini-powered answer generation

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/finbase-rag-assistant.git
cd finbase-rag-assistant
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run commands using `venv\Scripts\python.exe` or follow your organization's PowerShell execution-policy guidance.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root. Add your Gemini API key using the variable name expected by `src/llm.py`. For example:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Check `src/llm.py` to confirm the exact variable name used by your code. Never commit `.env` or publish real API keys. `.env.example` should contain placeholders only.

### 5. Add financial PDFs

Place PDFs you are authorized to use in:

```text
data/raw/
```

The current ingestion flow reads PDFs from this folder. Files in `data/raw/` are excluded from Git by the project's `.gitignore`, so add your own local documents after cloning.

## Run the Application

From the project root, try:

```bash
streamlit run src/streamlit_app.py
```

If your current code uses imports that assume the `src` directory is the working directory, run the command documented in the code or adjust the imports/package setup before deployment.

## RAG Workflow

1. **Ingestion:** PyMuPDF extracts text from each PDF page and records its source filename and page number.
2. **Chunking:** The text splitter divides long page text into smaller, overlapping chunks.
3. **Embedding:** Sentence Transformers converts each chunk into a numerical vector.
4. **Indexing:** FAISS indexes vectors to support similarity search.
5. **Retrieval:** A user's question is embedded and used to find relevant chunks.
6. **Generation:** The retrieved context and question are sent to Gemini to generate an answer.
7. **Response:** The assistant presents the answer and, when implemented, supporting source/page references.

## Evaluation

Evaluation assets are in `evaluation/`. Review `evaluation/eval.py` for the current evaluation procedure and `evaluation/eval_ques.json` for the questions being used. Record the metrics and test conditions when evaluation is run; do not report accuracy figures until they have been measured.

## Security and Privacy

- Keep API keys and credentials in `.env`; do not commit them.
- Never store passwords in plain text if authentication is added.
- For a multi-user version, associate each conversation and uploaded document with its owner and enforce access checks.
- Only upload documents you have permission to process.
- Review logs and error messages to ensure they do not expose sensitive financial information.

## Current Limitations / Planned Work

- Connect the Streamlit upload widget to the ingestion and indexing pipeline.
- Verify the full end-to-end question-answering flow.
- Persist and reload the FAISS index as appropriate.
- Display source citations for generated answers.
- Add secure user authentication and per-user chat history.
- Add automated evaluation and document the measured results.
- Prepare deployment configuration.

## Contributing

This is a learning and development project. For changes, create a branch, make a focused update, and test the affected pipeline stages before opening a pull request.

## License

No license has been specified yet. Add a license file before granting others explicit reuse permissions.
