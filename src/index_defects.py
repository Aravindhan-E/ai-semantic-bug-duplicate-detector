from pathlib import Path
import pandas as pd
from src.search import index_dataframe

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT/"data"/"synthetic_jira_defects.csv")
print(f"Indexed {index_dataframe(df)} defects.")
