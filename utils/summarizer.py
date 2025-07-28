from transformers import pipeline
from typing import List, Dict

class SubSectionSummarizer:
    def __init__(self):
        # Use a summarization pipeline from HuggingFace
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def extract_subsections(self, sections: List[Dict], persona: str, job_description: str) -> List[Dict]:
        """
        Generate refined summaries for each section using HuggingFace summarization.
        
        Args:
            sections (list): Top ranked sections with 'text', 'document', and 'page_number'.
            persona (str): Persona description
            job_description (str): Job/task description

        Returns:
            list: List of dicts containing document, page_number, and refined_text
        """
        sub_analysis = []

        for section in sections:
            try:
                content = section["text"]
                
                # Truncate if too long for model (~1024 tokens)
                if len(content) > 1000:
                    content = content[:1000]

                summary = self.summarizer(content, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

                sub_analysis.append({
                    "document": section["document"],
                    "page_number": section["page_number"],
                    "refined_text": summary
                })

            except Exception as e:
                print(f"   ✗ Error summarizing section from {section['document']}: {e}")
                continue

        return sub_analysis
