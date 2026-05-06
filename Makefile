.PHONY: bom bom-initial-csv bom-sheet

bom:
	@if [ ! -x analysis/local/regenerate_bom_outputs.sh ]; then \
		echo "Missing local order-derived BOM workflow: analysis/local/regenerate_bom_outputs.sh"; \
		echo "Use bom-initial-csv only for the old simple CSV workflow."; \
		exit 1; \
	fi
	analysis/local/regenerate_bom_outputs.sh

bom-initial-csv:
	python3 scripts/generate_bom.py --out notes/initial-bom.md

bom-sheet:
	python3 scripts/generate_bom.py --csv-url-file .bom-sheet-url --write-csv data/bom.csv --out notes/initial-bom.md
