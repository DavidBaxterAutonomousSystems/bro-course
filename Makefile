.PHONY: bom bom-sheet

bom:
	python3 scripts/generate_bom.py

bom-sheet:
	python3 scripts/generate_bom.py --csv-url-file .bom-sheet-url --write-csv data/bom.csv
