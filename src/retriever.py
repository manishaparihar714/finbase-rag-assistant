import pickle 
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


VECTORSTORE_PATH = Path("vectorstore")
INDEX_PATH = VECTORSTORE_PATH / "finbase.index"
CHUNKS_PATH = VECTORSTORE_PATH / "chunks.pkl"

MODEL_NAME = "BAAI/bge-small-en-v1.5"

def load_vstore():
    index=faiss.read_index(str(INDEX_PATH))

    with open(CHUNKS_PATH,"rb") as f:
        chunks=pickle.load(f)

    model=SentenceTransformer(MODEL_NAME)

    return index,chunks,model

def retrieve(query,top_k=5):
    index,chunks,model=load_vstore()

    query_embedding=model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    # Searching FAISS
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results=[]

    for score, index_id in zip(scores[0],indices[0]):
        if index_id == -1:
            continue

        results.append({
            "text": chunks[index_id]["text"],
            "source": chunks[index_id]["source"],
            "page": chunks[index_id]["page"],
            "score": float(score)
        })

    return results


if __name__ == "__main__":

    question = "What is the UPI transaction limit?"

    results = retrieve(question)

    print("\nQUESTION:")
    print(question)

    print("\nRETRIEVED RESULTS:")

    for i, result in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")
        print("Score:", result["score"])
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Text:")
        print(result["text"][:500])