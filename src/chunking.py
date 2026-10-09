from ingestion import pdf_loads 
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(documents):

    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks=[]

    for document in documents:
        split_texts= text_splitter.split_text(document["text"])

        for chunk in split_texts:
            chunks.append(
                {
                "text": chunk,
                "source": document["source"],
                "page": document["page"]
            })

    return chunks

if __name__== "__main__":
    documents=pdf_loads()

    chunks=create_chunks(documents)

    print(f"Total pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    print("\n----- SAMPLE CHUNK -----")
    print("Source:", chunks[0]["source"])
    print("Page:", chunks[0]["page"])
    print("Text:")
    print(chunks[0]["text"])