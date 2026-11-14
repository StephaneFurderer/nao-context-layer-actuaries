PY ?= python3

.PHONY: all setup data context check-sql grade talk slides clean

all: data context check-sql talk        ## everything that needs no LLM key

setup:                                  ## install Python deps (nao-core, duckdb<2)
	$(PY) -m pip install -r requirements.txt

data:                                   ## regenerate warehouse/travel.duckdb (seeded)
	$(PY) data/generate.py warehouse/travel.duckdb

context:                                ## nao sync: regenerate per-table context files
	cd context && nao sync

check-sql:                              ## run every reference SQL + the waterfall
	$(PY) evals/check_reference_sql.py

grade:                                  ## grade an answers folder: make grade ANSWERS=path
	$(PY) evals/grade.py $(ANSWERS)

talk:                                   ## validate every talking point is <= 60 s and evidenced
	$(PY) talk/check_talk.py

slides:                                 ## build the Slidev deck (needs Node 18+)
	cd slides && npm install && npx slidev build slides.md

chat:                                   ## nao chat UI at localhost:5005 (needs an LLM key)
	cd context && nao chat

test:                                   ## nao test against the agent (needs nao chat running + LLM key)
	cd context && nao test -k 3

clean:
	rm -f warehouse/travel.duckdb
