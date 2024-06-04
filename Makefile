# Makefile to run the tr.py Python script

# Define the Python interpreter and the script file
PYTHON := python
SCRIPT := files_cleaning.py

# Default target to execute the script
propre:
	$(PYTHON) $(SCRIPT)

# Clean target to remove any unwanted files (customize if needed)
clean:
	rm -f *.pyc
	rm -rf __pycache__

# Phony targets
.PHONY: run clean
