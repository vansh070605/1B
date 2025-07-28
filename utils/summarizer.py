from transformers import pipeline
from typing import List, Dict


class SubSectionSummarizer:
    def __init__(self):
        # Lightweight summarization model (under 500MB)
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def extract_subsections(self, sections: List[Dict], persona: str, job_description: str) -> List[Dict]:
        """
        Refines top sections by summarizing them in context of persona and job.

        Args:
            sections (List[Dict]): List of extracted document sections.
            persona (str): Persona context for the summarization.
            job_description (str): Task context for prompting.

        Returns:
            list: Refined summaries with metadata.
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
                doc = section.get("document", "unknown")
                page = section.get("page_number", 0)

                if not content or len(content) < 10:
                    continue

                # Avoid duplicates
                dedup_key = (doc, page, content)
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

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

                sub_analysis.append({
                    "document": doc,
                    "page_number": page,
                    "refined_text": summary
                })
            except Exception as e:
                print(f"   ✗ Error summarizing section from {doc} (page {page}): {e}")
                continue

        return sub_analysis
