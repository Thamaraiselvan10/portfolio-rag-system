from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
NEWS_DIR = DATA_DIR / "news"
PORTFOLIO_PATH = DATA_DIR / "portfolio.json"
GLOSSARY_PATH = DATA_DIR / "glossary.md"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3