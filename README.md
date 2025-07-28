# Persona-Driven Document Analysis & Section Ranking  
**Adobe India Hackathon 2025 — Round 1B "Connecting the Dots"**

## Overview  
A pipeline that processes a set of PDF documents, extracts heading-like sections, ranks them by relevance to a given persona and job description, and generates concise summaries of top sections.

## Features  
- **Section Extraction**: Scans each page for title-case lines as candidate headings and captures full page text (extractor.py).  
- **Relevance Scoring**: Embeds combined section title + text and a “Persona: Research Analyst. Job: Analyze the provided documents …” query via Sentence-Transformers and ranks sections by cosine similarity (scorer.py).  
- **Subsection Summarization**: Summarizes top-ranked sections using Hugging Face’s DistilBART model to produce refined insights per document and page (summarizer.py).

## Input & Output  
- **Input**:  
  - PDF files in `/input` (e.g., “South of France – Cities.pdf”, “…Cuisine.pdf”, etc.)  
  - `persona` and `job_to_be_done` values embedded in `analysis.json` metadata  
- **Output**:  
  - Ranked section list with `document`, `page_number`, `section_title`, and `score`  
  - `sub_section_analysis`: `document`, `page_number`, and `refined_text` summaries  

## Quick Start  
1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
2. **Run extraction, scoring & summarization**  
   ```bash
   python extractor.py input/  
   python scorer.py  # reads sections, ranks by persona/job  
   python summarizer.py  # summarizes top sections  
   ```
3. **Review outputs**  
   - `analysis.json` contains metadata, ranked sections, and summaries.  
# Persona-Driven Document Analysis & Section Ranking  
**Adobe India Hackathon 2025 — Round 1B "Connecting the Dots"**

## Overview  
A pipeline that processes a set of PDF documents, extracts heading-like sections, ranks them by relevance to a given persona and job description, and generates concise summaries of top sections.

## Approach Explanation  
This solution is built as a modular, three-stage pipeline for persona-driven document intelligence:

1. **Section Extraction**  
   - Each PDF is parsed page by page to identify candidate headings (typically title-case lines) and their associated content.
   - Implemented in `extractor.py`, which outputs structured section data including document name, page number, section title, and text.

2. **Relevance Scoring**  
   - Each extracted section is embedded using Sentence-Transformers.
   - The persona and job description are combined into a query embedding.
   - Sections are ranked by cosine similarity to this query, prioritizing those most relevant to the persona’s needs.
   - Implemented in `scorer.py`.

3. **Subsection Summarization**  
   - The top-ranked sections are summarized using a transformer-based summarization model (DistilBART via Hugging Face).
   - This produces concise, persona-tailored insights for each key section.
   - Implemented in `summarizer.py`.

All results, including metadata, ranked sections, and summaries, are consolidated into `analysis.json` for easy review and downstream use.

## Features  
- **Section Extraction**: Scans each page for title-case lines as candidate headings and captures full page text (`extractor.py`).  
- **Relevance Scoring**: Embeds combined section title + text and a persona/job query via Sentence-Transformers, ranking sections by cosine similarity (`scorer.py`).  
- **Subsection Summarization**: Summarizes top-ranked sections using Hugging Face’s DistilBART model to produce refined insights per document and page (`summarizer.py`).

## Input & Output  
- **Input**:  
  - PDF files in `/input` (e.g., “South of France – Cities.pdf”, “…Cuisine.pdf”, etc.)  
  - `persona` and `job_to_be_done` values embedded in `analysis.json` metadata  
- **Output**:  
  - Ranked section list with `document`, `page_number`, `section_title`, and `score`  
  - `sub_section_analysis`: `document`, `page_number`, and `refined_text` summaries  

## Quick Start  
1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
2. **Run extraction, scoring & summarization**  
   ```bash
   python extractor.py input/  
   python scorer.py  # reads sections, ranks by persona/job  
   python summarizer.py  # summarizes top sections  
   ```
3. **Review outputs**  
   - `analysis.json` contains metadata, ranked sections, and summaries.  

## Project Structure  
```
├── main.py             # Orchestrates the full pipeline (extraction, scoring, summarization)
├── extractor.py        # Extracts section candidates from PDFs  
├── scorer.py           # Ranks sections by persona relevance  
├── summarizer.py       # Summarizes top sections  
├── utils/              # Utility modules for extraction, scoring, summarization
│   ├── extractor.py
│   ├── scorer.py
│   └── summarizer.py
├── requirements.txt    # Python dependencies  
├── input/              # Input PDFs and optional config files
│   ├── *.pdf
│   └── config.json / input.json / persona.json
├── output/             # Output directory for results
│   └── analysis.json   # Metadata, ranked sections, and summaries  
```

## Dependencies  
- PyMuPDF ≥ 1.24.0  
- sentence-transformers==2.2.2, scikit-learn==1.3.0, numpy ≥ 1.24.0  
- spacy ≥ 3.6.0, nltk ≥ 3.8.0  
- pandas ≥ 2.0.0, regex ≥ 2023.6.0  
- transformers (for summarization)

## How It Works  
- Place your PDF files in the `input/` directory.
- (Optional) Add a `config.json` in `input/` to specify `persona` and `job_to_be_done`.
- Run the pipeline using `main.py` or the individual scripts for each stage.
- Results are saved in `output/analysis.json` with all extracted, ranked, and summarized information.

## License  
Built for Adobe India Hackathon 2025 — Round 1B. Please refer to competition guidelines for
## Project Structure  
```
├── extractor.py        # Extracts section candidates from PDFs  
├── scorer.py           # Ranks sections by persona relevance  
├── summarizer.py       # Summarizes top sections  
├── requirements.txt    # Python dependencies  
└── analysis.json       # Metadata, ranked sections, and summaries  
```

## Dependencies  
- PyMuPDF ≥ 1.24.0  
- sentence-transformers==2.2.2, scikit-learn==1.3.0, numpy ≥ 1.24.0  
- spacy ≥ 3.6.0, nltk ≥ 3.8.0  
- pandas ≥ 2.0.0, regex ≥ 2023.6.0  

## License  
Built for Adobe India Hackathon 2025 — Round 1B. Please refer to competition guidelines for usage.
