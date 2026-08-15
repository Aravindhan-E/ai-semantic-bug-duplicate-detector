# AI Semantic Bug Duplicate Detector — Phase 3

Phase 3 adds a more realistic evaluation set where multiple historical defects can be valid matches, plus reviewer feedback in the Streamlit UI.

Run:
```bat
python src\index_defects.py
streamlit run app.py --server.fileWatcherType none
```

Evaluation:
```bat
python -m src.evaluate
```

Metrics:
- Hit@1
- Hit@3
- Hit@5
- MRR

Reviewer choices:
- Confirm duplicate
- Not duplicate
- Related

The dataset is synthetic Jira-style data and contains no proprietary company information.
