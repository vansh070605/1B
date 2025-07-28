# Approach Explanation: Persona-Driven Document Intelligence

## Methodology Overview

Our solution implements a three-stage pipeline that intelligently extracts and prioritizes document sections based on persona-specific requirements and job-to-be-done contexts.

### Stage 1: Intelligent Section Extraction
We employ PyMuPDF for robust PDF parsing with a sophisticated heading detection algorithm. The system identifies section candidates using two heuristics: (1) numbered patterns (e.g., "1.2", "3.1.1") and (2) title-case formatting with length constraints (4-80 characters). This approach ensures we capture both structured academic content and narrative sections while avoiding false positives from regular text.

### Stage 2: Semantic Relevance Scoring
The core innovation lies in our persona-aware ranking system using Sentence Transformers (all-MiniLM-L6-v2). We create a unified query embedding combining the persona description and job requirements, then compute cosine similarity against each section's combined title and content. This semantic approach outperforms keyword matching by understanding context and intent, enabling the system to work across diverse domains without domain-specific tuning.

### Stage 3: Contextual Summarization
For the top-ranked sections, we employ DistilBART-CNN-12-6 for intelligent summarization. The system incorporates persona and job context into the summarization prompt, ensuring outputs are tailored to the user's specific needs. We implement intelligent text truncation at sentence boundaries to respect model input limits while preserving semantic coherence.

## Technical Architecture

The solution is designed for CPU-only execution with strict resource constraints. We use lightweight models (all-MiniLM-L6-v2: ~90MB, DistilBART-CNN-12-6: ~500MB) to stay under the 1GB limit while maintaining high performance. The modular architecture allows independent optimization of each stage and easy extension to new document types or personas.

## Key Innovations

1. **Persona-Contextual Processing**: Unlike generic document analysis, our system tailors every stage to the specific user persona and task requirements.

2. **Semantic Understanding**: Sentence transformers enable the system to understand nuanced relationships between content and user needs, rather than relying on simple keyword matching.

3. **Intelligent Deduplication**: Multi-level deduplication prevents redundant analysis while preserving important variations in content.

4. **Robust Error Handling**: Graceful degradation ensures the system continues processing even when individual sections fail, maintaining overall reliability.

This approach delivers a generic, scalable solution that can handle diverse document collections, personas, and job requirements while meeting all technical constraints. 