# AI Semantic Bug Duplicate Detector

An AI-assisted QA tool that identifies potentially duplicate Jira-style defects using semantic embeddings and vector similarity search.

## Problem Statement

In a QA environment, a newly reported defect may already exist in the defect repository with different wording.

Traditional keyword-based searches may fail to identify these semantically similar defects.

This project provides a semantic search-based assistant that helps QA engineers find potentially duplicate historical defects before logging a new defect.

## Solution

The application:

1. Accepts a new defect title and description.
2. Converts the defect text into an embedding using Sentence Transformers.
3. Searches historical defect embeddings stored in ChromaDB.
4. Retrieves the Top-K most similar defects.
5. Calculates a similarity score for each result.
6. Applies a configurable similarity threshold.
7. Allows a QA reviewer to classify the result as:
   - Confirm duplicate
   - Not duplicate
   - Related
8. Persists reviewer decisions for traceability.

## Architecture

```text
                     New Defect
                         |
                         v
                 +---------------+
                 | Streamlit UI  |
                 +-------+-------+
                         |
                         v
              +-------------------------+
              | Sentence Transformers  |
              |   Text -> Embedding     |
              +------------+------------+
                           |
                           v
                    +-------------+
                    |   ChromaDB  |
                    | Vector Store|
                    +------+------+ 
                           |
                           v
                 Semantic Similarity
                       Search
                           |
                           v
                     Top-K Results
                           |
                           v
                 Similarity Threshold
                           |
                           v
                     QA Reviewer
                    /     |      \
                   /      |       \
          Duplicate   Related   Not Duplicate
                           |
                           v
                  Reviewer Feedback
```

## Tech Stack

- **Python**
- **Streamlit**
- **Sentence Transformers**
- **ChromaDB**
- **Pandas**
- **scikit-learn**

## Key Features

- Semantic defect similarity search
- Sentence Transformer embeddings
- ChromaDB vector database
- Top-K retrieval
- Configurable similarity threshold
- Synthetic Jira-style defect repository
- CSV-based defect ingestion
- Human-in-the-loop reviewer workflow
- Persistent reviewer feedback
- Retrieval evaluation using Hit@1, Hit@3, Hit@5 and MRR

## Evaluation

The project includes a labeled synthetic evaluation dataset where multiple historical defects can be considered acceptable matches.

### Evaluation Metrics

| Metric | Result |
|---|---:|
| Hit@1 | 100% |
| Hit@3 | 100% |
| Hit@5 | 100% |
| MRR | 1.000 |

> **Note:** These results are from a small synthetic evaluation dataset and should not be interpreted as production accuracy.

## Reviewer Workflow

The system is designed as a QA assistant rather than an automatic duplicate detector.

A high similarity score indicates that a historical defect may be related, but it does not prove that both defects have the same root cause.

The QA reviewer can make the final decision:

- **Confirm duplicate**
- **Not duplicate**
- **Related**

Reviewer decisions are persisted for traceability.

## Example Workflow

```text
New Defect
    |
    v
Generate Embedding
    |
    v
Search Historical Defects
    |
    v
Retrieve Top-K Results
    |
    v
Apply Similarity Threshold
    |
    v
QA Reviewer Validation
    |
    v
Store Reviewer Decision
```

## Project Structure

```text
ai-semantic-bug-duplicate-detector/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── synthetic_jira_defects.csv
│   └── evaluation_pairs.csv
│
└── src/
    ├── __init__.py
    ├── search.py
    ├── index_defects.py
    └── evaluate.py
```

## How to Run

### 1. Create a virtual environment

```bat
python -m venv .venv
```

### 2. Activate the virtual environment

Windows:

```bat
.venv\Scripts\activate
```

### 3. Install dependencies

```bat
pip install -r requirements.txt
```

### 4. Create the vector index

```bat
python -m src.index_defects
```

### 5. Start the Streamlit application

```bat
streamlit run app.py --server.fileWatcherType none
```

### 6. Run evaluation

```bat
python -m src.evaluate
```

## Testing Approach

The application was tested using positive, negative and edge-case scenarios.

### Positive Scenarios

- Defects with similar meaning
- Different wording describing a similar issue
- Historical defects that should be retrieved as potential matches

### Negative Scenarios

- Completely unrelated defects
- Similar wording but different context

### Edge Cases

- Empty defect input
- Very short descriptions
- Similarity threshold boundaries
- Different Top-K values
- Invalid CSV data
- Incomplete CSV data
- Reviewer decision persistence

## Limitations

- The current dataset contains synthetic Jira-style defects.
- The evaluation dataset is small.
- Semantic similarity does not guarantee identical root cause.
- The current version does not directly integrate with Jira APIs.
- Reviewer feedback is persisted but is not currently used to retrain the embedding model.

## Future Enhancements

- Jira REST API integration
- Automatic defect ingestion
- Authentication and role-based access
- Larger real-world evaluation dataset
- Similarity threshold tuning using validation data
- Reviewer analytics
- Hybrid semantic and metadata-based search
- Docker-based deployment
- Cloud deployment

## Data Disclaimer

This project uses **synthetic Jira-style defect data** created for demonstration and testing purposes.

It contains **no proprietary company information or confidential production defects**.

## Author

**Aravindhan E**

QA / Automation Engineer