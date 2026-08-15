from pathlib import Path
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "chroma_db"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "jira_defects"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def build_texts(df):
    return (df["title"].fillna("") + ". " + df["description"].fillna("") +
            ". Module: " + df["module"].fillna("")).tolist()

def index_dataframe(df):
    required = {"bug_id","title","description","module","severity","status"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df = df.copy().fillna("")
    embeddings = get_model().encode(build_texts(df), normalize_embeddings=True).tolist()
    client = chromadb.PersistentClient(path=str(DB))
    try: client.delete_collection(COLLECTION_NAME)
    except Exception: pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space":"cosine"})
    collection.add(
        ids=df["bug_id"].astype(str).tolist(),
        embeddings=embeddings,
        documents=build_texts(df),
        metadatas=df[["title","description","module","severity","status"]].to_dict("records"))
    return len(df)

def search_similar(title, description, top_k=5):
    collection = chromadb.PersistentClient(path=str(DB)).get_collection(COLLECTION_NAME)
    query = f"{title}. {description}"
    emb = get_model().encode([query], normalize_embeddings=True).tolist()
    r = collection.query(query_embeddings=emb, n_results=top_k,
                         include=["metadatas","distances"])
    return [{"bug_id":bid, "similarity":max(0,min(1,1-float(dist))), **meta}
            for bid, meta, dist in zip(r["ids"][0], r["metadatas"][0], r["distances"][0])]
