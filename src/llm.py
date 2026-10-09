import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()


def get_llm():

    api_key= os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("Therr is not api key set in .env file")

    llm= ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0
    )

    return llm
 
if __name__== "__main__":
    llm=get_llm()
    print("\n llm successfully loaded !")

    response=llm.invoke("explain upi transaction in one sentence?")
    print("Assistant : \n")
    print(response.content[0] ["text"])