import pandas as pd
from pathlib import Path
from src.search import search_similar
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data"/"evaluation_pairs.csv")
rows=[]
for _,q in df.iterrows():
    acceptable=set(q["acceptable_bug_ids"].split("|"))
    ids=[x["bug_id"] for x in search_similar(q["query_title"],q["query_description"],5)]
    rank=next((i for i,x in enumerate(ids,1) if x in acceptable),0)
    rows.append({"query_id":q["query_id"],"acceptable":q["acceptable_bug_ids"],
                 "top1":ids[0] if ids else "", "hit_at_1":int(rank==1),
                 "hit_at_3":int(0<rank<=3),"hit_at_5":int(0<rank<=5),
                 "reciprocal_rank":1/rank if rank else 0})
out=pd.DataFrame(rows)
print("\n=== Phase 3 Semantic Retrieval Evaluation ===")
print(f"Queries evaluated : {len(out)}")
print(f"Hit@1             : {out.hit_at_1.mean():.2%}")
print(f"Hit@3             : {out.hit_at_3.mean():.2%}")
print(f"Hit@5             : {out.hit_at_5.mean():.2%}")
print(f"MRR               : {out.reciprocal_rank.mean():.3f}")
print("\nPer-query results:")
print(out.to_string(index=False))
