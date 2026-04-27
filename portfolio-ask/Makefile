# ----------------------------
# Setup environment
# ----------------------------
setup:
	python -m venv venv
	venv\Scripts\python -m pip install --upgrade pip
	venv\Scripts\pip install -r requirements.txt


# ----------------------------
# Run default query
# ----------------------------
run:
	venv\Scripts\python -m portfolio_ask "Which stock has highest investment value?"


# ----------------------------
# Run custom query
# Usage: make query q="your question"
# ----------------------------
query:
	venv\Scripts\python -m portfolio_ask "$(q)"


# ----------------------------
# Evaluate system
# ----------------------------
eval:
	venv\Scripts\python tests/eval.py


# ----------------------------
# Clean cache files
# ----------------------------
clean:
	del /s /q __pycache__ 2>nul || exit 0
	del /s /q *.pyc 2>nul || exit 0