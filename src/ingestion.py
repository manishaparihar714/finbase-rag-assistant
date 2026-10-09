import pymupdf
from pathlib import Path 
import re

def clean_text(text):

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = text.strip()

    return text

def pdf_loads(data_path="data/raw"):
    documents=[]

    pdf_files=Path(data_path).glob("*.pdf")

    seen_text = set()

    for pdf_path in pdf_files:
        pdf=pymupdf.open(pdf_path)

        for page_number, page in enumerate(pdf,start =1 ):
            text = page.get_text("text").strip()

             # Skip empty pages
            if not text:
                continue

            # Clean extracted text
            text = clean_text(text)

            # Skip very small/meaningless content
            if len(text) < 50:
                continue

            # Remove duplicate page content
            text_key = text.lower()

            if text_key in seen_text:
                continue

            seen_text.add(text_key)

            
            documents.append(
                {
                    "text":text,
                    "source":pdf_path.name,
                    "page":page_number
                }
            )

        pdf.close()

    return documents

if __name__== "__main__":
    documents= pdf_loads()

    print(f"total No. of pages: {len(documents)}")

    for doc in documents[:3]:
        print("\n-------------------------")
        print("Source:", doc["source"])
        print("Page:", doc["page"])
        print(doc["text"][:500])
