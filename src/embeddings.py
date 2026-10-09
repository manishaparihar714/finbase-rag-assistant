from sentence_transformers import SentenceTransformer
from chunking import create_chunks 
from ingestion import pdf_loads

MODEL_NAME = "BAAI/bge-small-en-v1.5"

def create_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)
    
    texts= [chunk["text"] for chunk in chunks]

    embeddings= model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings

if __name__=="__main__":
    documents= pdf_loads()

    chunks=create_chunks(documents)

    embeddings = create_embeddings(chunks)

    print("\nEmbedding complete!")
    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)