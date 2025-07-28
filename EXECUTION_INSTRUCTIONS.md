# Execution Instructions

## Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized execution)

## Local Execution

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv persona_env
source persona_env/bin/activate  # On Windows: persona_env\Scripts\activate

# Install dependencies
pip install -r requirement.txt
```

### 2. Prepare Input
- Place PDF documents in the `input/` directory
- Optionally create a `config.json` file in `input/` with:
```json
{
  "persona": "PhD Researcher in Computational Biology",
  "job_to_be_done": "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
}
```

### 3. Run Analysis
```bash
python main.py
```

### 4. View Results
- Check `output/analysis.json` for the complete analysis
- Review ranked sections and sub-section summaries

## Docker Execution

### 1. Build Image
```bash
docker build -t persona-analyzer .
```

### 2. Run Container
```bash
# Mount input and output directories
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output persona-analyzer
```

### 3. View Results
- Results will be available in the `output/` directory on your host machine

## Test Mode
```bash
# Run with test configuration
python main.py --test
```

## Configuration Options

### Environment Variables
- `PERSONA`: Default persona if no config file is provided
- `JOB_DESCRIPTION`: Default job description if no config file is provided

### Input Configuration
Create `input/config.json` to customize:
- `persona`: The user persona for analysis
- `job_to_be_done`: The specific task to accomplish

## Expected Output
The system generates `output/analysis.json` containing:
- Metadata (input documents, persona, job, timestamp)
- Ranked sections with importance scores
- Sub-section analysis with refined summaries

## Performance Notes
- Processing time: ≤ 60 seconds for 3-5 documents
- Model size: ≤ 1GB total
- CPU-only execution
- No internet access required during runtime 