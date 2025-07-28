from transformers import pipeline
from typing import List, Dict


class SubSectionSummarizer:
    def __init__(self):
        # Initialize the summarizer pipeline with a pre-trained model
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def extract_subsections(self, sections: List[Dict], persona: str, job_description: str) -> List[Dict]:
        """
        Generate refined summaries for each unique section.

        Args:
            sections (List[Dict]): List of extracted document sections.
            persona (str): Persona context for the summarization (can be extended).
            job_description (str): Task context (can be used for prompting).

        Returns:
            List[Dict]: List of summarized sub-sections.
        """
        sub_analysis = []
        seen = set()

        for section in sections:
            try:
                content = section.get("text", "").strip()
                doc = section.get("document", "unknown")
                page = section.get("page_number", 0)

                if not content or len(content) < 10:
                    continue

                # Avoid duplicates
                dedup_key = (doc, page, content)
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                # Truncate overly long content for the model
                input_text = content if len(content) < 1000 else content[:1000]

                summary = self.summarizer(
                    input_text,
                    max_length=150,
                    min_length=40,
                    do_sample=False
                )[0]["summary_text"]

                sub_analysis.append({
                    "document": doc,
                    "page_number": page,
                    "refined_text": summary
                })

            except Exception as e:
                print(f"   ✗ Error summarizing section from {doc} (page {page}): {e}")
                continue

        return sub_analysis
