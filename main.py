import os
import json
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Import utility modules
from utils.extractor import DocumentExtractor
from utils.scorer import SectionScorer
from utils.summarizer import SubSectionSummarizer

class PersonaDrivenAnalyzer:
    """Main analyzer that orchestrates the persona-driven document intelligence"""
    
    def __init__(self):
        self.ranker = SectionScorer()
        self.summarizer = SubSectionSummarizer()
    
    def process_collection(self, pdf_paths: List[str], persona: str, job_description: str) -> Dict[str, Any]:
        print(f"Processing {len(pdf_paths)} documents for persona: {persona}")
        print(f"Job to be done: {job_description}")
        
        print("\n1. Extracting sections from documents...")
        all_sections = []
        
        for pdf_path in pdf_paths:
            try:
                print(f"   Processing: {os.path.basename(pdf_path)}")
                extractor = DocumentExtractor(pdf_path)
                sections = extractor.extract_sections()
                all_sections.extend(sections)
                print(f"   ✓ Extracted {len(sections)} sections")
            except Exception as e:
                print(f"   ✗ Error processing {pdf_path}: {str(e)}")
                continue
        
        if not all_sections:
            raise Exception("No sections could be extracted from any document")
        
        print(f"Total sections extracted: {len(all_sections)}")
        
        print("\n2. Ranking sections by relevance...")
        ranked_sections = self.ranker.rank_sections(all_sections, persona, job_description)
        top_sections = ranked_sections[:20]
        print(f"Selected top {len(top_sections)} most relevant sections")
        
        print("\n3. Analyzing sub-sections...")
        sub_section_analysis = self.summarizer.extract_subsections(
            top_sections[:10], persona, job_description
        )
        
        result = self._format_output(
            pdf_paths, persona, job_description, 
            top_sections, sub_section_analysis
        )
        
        print(f"✓ Analysis complete! Generated {len(result['extracted_sections'])} section rankings")
        print(f"✓ Generated {len(result['sub_section_analysis'])} sub-section analyses")
        
        return result
    
    def _format_output(self, pdf_paths: List[str], persona: str, job_description: str,
                      sections: List[Dict], sub_sections: List[Dict]) -> Dict[str, Any]:
        return {
            "metadata": {
                "input_documents": [os.path.basename(path) for path in pdf_paths],
                "persona": persona,
                "job_to_be_done": job_description,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": [
                {
                    "document": section["document"],
                    "page_number": section["page_number"],
                    "section_title": section["section_title"],
                    "importance_rank": idx + 1
                }
                for idx, section in enumerate(sections)
            ],
            "sub_section_analysis": [
                {
                    "document": sub_section["document"],
                    "refined_text": sub_section["refined_text"],
                    "page_number": sub_section["page_number"]
                }
                for sub_section in sub_sections
            ]
        }

def load_input_config() -> Dict[str, Any]:
    input_dir = Path("input")
    config_files = ["config.json", "input.json", "persona.json"]
    config_data = None

    for config_file in config_files:
        config_path = input_dir / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                print(f"Loaded configuration from: {config_file}")
                break
            except Exception as e:
                print(f"Error reading {config_file}: {str(e)}")
                continue

    if not config_data:
        config_data = {
            "persona": os.getenv("PERSONA", "Research Analyst"),
            "job_to_be_done": os.getenv("JOB_DESCRIPTION", 
                              "Analyze the provided documents and extract key insights")
        }
        print("Using default/environment configuration")

    return config_data

def find_pdf_files(input_dir: Path) -> List[str]:
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        raise Exception(f"No PDF files found in {input_dir}")

    if len(pdf_files) > 10:
        print(f"Warning: Found {len(pdf_files)} PDFs, using first 10")
        pdf_files = pdf_files[:10]

    return [str(pdf) for pdf in sorted(pdf_files)]

def main():
    try:
        print("=" * 60)
        print("Round 1B: Persona-Driven Document Intelligence")
        print("=" * 60)
        
        input_dir = Path("input")
        output_dir = Path("output")

        if not input_dir.exists():
            print(f"Error: Input directory {input_dir} not found")
            sys.exit(1)

        output_dir.mkdir(parents=True, exist_ok=True)

        print("\nLoading configuration...")
        config = load_input_config()
        persona = config.get("persona", "Research Analyst")
        job_description = config.get("job_to_be_done", "Analyze documents and extract insights")

        print("\nFinding PDF files...")
        pdf_files = find_pdf_files(input_dir)
        print(f"Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"  - {os.path.basename(pdf)}")

        print("\nInitializing analyzer...")
        analyzer = PersonaDrivenAnalyzer()

        print("\nStarting analysis...")
        start_time = datetime.now()

        result = analyzer.process_collection(pdf_files, persona, job_description)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        print(f"\nProcessing completed in {processing_time:.2f} seconds")

        if processing_time > 60:
            print(f"Warning: Processing time ({processing_time:.2f}s) exceeded 60s limit")

        output_file = output_dir / "analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Results saved to: {output_file}")
        print(f"✓ Extracted {len(result['extracted_sections'])} relevant sections")
        print(f"✓ Generated {len(result['sub_section_analysis'])} sub-section analyses")

        print("\nAnalysis Summary:")
        print(f"  Documents processed: {len(result['metadata']['input_documents'])}")
        print(f"  Persona: {result['metadata']['persona']}")
        print(f"  Job: {result['metadata']['job_to_be_done'][:100]}...")
        print(f"  Processing time: {processing_time:.2f}s")

        print("\n" + "=" * 60)
        print("Analysis completed successfully!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nDetailed error information:")
        traceback.print_exc()
        sys.exit(1)

def test_mode():
    print("Running in test mode...")

    test_config = {
        "persona": "PhD Researcher in Computational Biology",
        "job_to_be_done": "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    }

    input_dir = Path("input")
    if input_dir.exists():
        with open(input_dir / "config.json", 'w') as f:
            json.dump(test_config, f, indent=2)
        print("Created test configuration")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_mode()
    else:
        main()
