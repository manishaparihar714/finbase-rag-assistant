from retriever import retrieve
from llm import get_llm

SYSTEM_PROMPT = """
You are FinBase's AI-powered financial customer support assistant.

Your job is to answer the user's question using ONLY the provided
knowledge-base context.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the context does not contain enough information to answer the
   question, clearly say that the information is not available in
   the provided knowledge base.
4. Give a concise and helpful answer.
5. When possible, mention the relevant source and page.
"""

def answer_ques(question, top_k=5):
    results = retrieve(question, top_k=top_k)

    context_parts=[]

    for result in results:
        context_parts.append(
            f"""
Source:{result['source']}
Page:{result["page"]}
Content:{result["text"]}

"""
        )

    context="\n".join(context_parts)

    prompt=f"""
{SYSTEM_PROMPT}
KNOWLEDGE BASE CONTEXT:{context}
USER QUESTION:
{question}

ANSWER:
"""
    llm=get_llm()
    response=llm.invoke(prompt)
    return{
        "answer":response.content[0]["text"],
        "sources":results
    }

if __name__ == "__main__":

    question = "When does an account become dormant due to inactivity?"

    result = answer_ques(question)

    print("\nAssistant:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} | "
            f"Page {source['page']} | "
            f"Score: {source['score']:.4f}"
        )