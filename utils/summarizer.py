from transformers import pipeline
from typing import List, Dict


class SubSectionSummarizer:
    def __init__(self):
<<<<<<< HEAD
        # Initialize the summarizer pipeline with a pre-trained model
=======
        # Lightweight summarization model (under 500MB)
>>>>>>> bcd4d18a44732faafd626984dad87d1912a3fe60
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def extract_subsections(self, sections: List[Dict], persona: str, job_description: str) -> List[Dict]:
        """
<<<<<<< HEAD
        Generate refined summaries for each unique section.
=======
        Refines top sections by summarizing them in context of persona and job.
>>>>>>> bcd4d18a44732faafd626984dad87d1912a3fe60

        Args:
            sections (List[Dict]): List of extracted document sections.
            persona (str): Persona context for the summarization (can be extended).
            job_description (str): Task context (can be used for prompting).

        Returns:
<<<<<<< HEAD
            List[Dict]: List of summarized sub-sections.
=======
            list: Refined summaries with metadata.
>>>>>>> bcd4d18a44732faafd626984dad87d1912a3fe60
        """
        sub_analysis = []
        seen = set()

        system_prompt = (
            f"You are assisting a persona: {persona}.\n"
            f"The task is: {job_description}.\n"
            f"Summarize the section focusing on what's most relevant."
        )

        for section in sections:
            try:
                content = section.get("text", "").strip()
<<<<<<< HEAD
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
=======

                if not content:
                    continue

                # Truncate intelligently to ~1000 chars with sentence boundary
                if len(content) > 1000:
                    truncated = content[:1000].rsplit('.', 1)[0]
                    content = truncated + '.' if truncated else content[:1000]

                # Combine context + content
                combined_input = system_prompt + "\n\n" + content

                summary = self.summarizer(
                    combined_input,
                    max_length=160,
                    min_length=40,
                    do_sample=False
                )[0]["summary_text"].strip()
>>>>>>> bcd4d18a44732faafd626984dad87d1912a3fe60

                sub_analysis.append({
                    "document": doc,
                    "page_number": page,
                    "refined_text": summary
                })
            except Exception as e:
                print(f"   ✗ Error summarizing section from {doc} (page {page}): {e}")
                continue

        return sub_analysis
