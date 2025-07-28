from sentence_transformers import SentenceTransformer, util

class SectionScorer:
    def __init__(self):
        # Load the pre-trained sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def rank_sections(self, sections, persona, job_description):
        """
        Rank document sections by relevance to a persona and their job description.

        Args:
            sections (list): List of section dicts with keys: section_title, text, etc.
            persona (str): Persona description
            job_description (str): Task to be done

        Returns:
            List of sections ranked by relevance (high to low)
        """

        # Combine heading + body for embeddings
        section_texts = [
            f"{sec['section_title']} {sec['text']}" for sec in sections
        ]

        # Create a query embedding for the combined persona + job
        query = f"Persona: {persona}. Job: {job_description}"
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        # Encode all sections
        section_embeddings = self.model.encode(section_texts, convert_to_tensor=True)

        # Compute cosine similarity scores
        similarities = util.pytorch_cos_sim(query_embedding, section_embeddings)[0]

        # Attach scores to each section
        for idx, score in enumerate(similarities):
            sections[idx]['score'] = float(score)

        # Sort the sections in descending order of relevance
        ranked_sections = sorted(sections, key=lambda x: x['score'], reverse=True)

        return ranked_sections
