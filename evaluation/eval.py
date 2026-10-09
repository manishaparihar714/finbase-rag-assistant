import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from rag import answer_ques


# Load evaluation questions
with open("evaluation/eval_ques.json", "r", encoding="utf-8") as f:
    evaluation_data = json.load(f)


def evaluate_retrieval():

    total_questions = len(evaluation_data)

    correct_source = 0
    correct_page = 0

    print("\n========== RAG EVALUATION ==========\n")

    for item in evaluation_data:

        question = item["question"]
        expected_source = item["expected_source"]
        expected_page = item["expected_page"]

        print(f"Question: {question}")

        result = answer_ques(question, top_k=5)

        sources = result["sources"]

        retrieved_sources = [
            source["source"]
            for source in sources
        ]

        retrieved_pages = [
            source["page"]
            for source in sources
        ]

        # Check whether expected PDF was retrieved
        source_found = expected_source in retrieved_sources

        # Check whether expected page was retrieved
        page_found = expected_page in retrieved_pages

        if source_found:
            correct_source += 1

        if page_found:
            correct_page += 1

        print("Expected source:", expected_source)
        print("Retrieved sources:", retrieved_sources)

        print("Source correct:", source_found)
        print("Page correct:", page_found)

        print("-" * 60)

    source_accuracy = correct_source / total_questions
    page_accuracy = correct_page / total_questions

    print("\n========== RESULTS ==========")

    print(
        f"Source Retrieval Accuracy: "
        f"{source_accuracy * 100:.2f}%"
    )

    print(
        f"Page Retrieval Accuracy: "
        f"{page_accuracy * 100:.2f}%"
    )


if __name__ == "__main__":
    evaluate_retrieval()