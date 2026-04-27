import sys
from portfolio_ask.main import run
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m portfolio_ask \"your query\"")
    else:
        result = run(sys.argv[1])
        print(json.dumps(result, indent=2))