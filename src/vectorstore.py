import pickle
from pathlib import Path

import faiss

from ingestion import pdf_loads
from chunking import create_chunks 
from embeddings import create_embeddings

vstore_path=Path("vectorstore")
INDEX_PATH = vstore_path/ "finbase.index"
CHUNKS_PATH = vstore_path / "chunks.pkl"


def built_vstore():
    documents=pdf_loads()
    chunks=create_chunks(documents)
    embeddings=create_embeddings(chunks)

    dimension=embeddings.shape[1]

    index=faiss.IndexFlatIP(dimension)
    embeddings=embeddings.astype("float32")

    index.add(embeddings)
    vstore_path.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("Vector store created successfully!")
    print("Number of vectors:", index.ntotal)
    print("Vector dimension:", dimension)
    print("Index saved to:", INDEX_PATH)
    print("Chunks saved to:", CHUNKS_PATH)
  


if __name__ == "__main__":
    built_vstore()