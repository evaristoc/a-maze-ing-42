# Define the path to the virtual environment's python/pip
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: setup sync clean

# 1. The 'setup' command: Checks if .venv exists, creates it, and installs
setup:
	@test -d $(VENV) || (echo "Creating .venv..." && python3 -m venv $(VENV))
	@$(PIP) install --upgrade pip
# 	@$(PIP) install -e .
	@chmod +x setup.sh
	./setup.sh
	@echo "Handshake complete. Dependencies are synced."

# 2. The 'sync' command: Use this when a teammate pulls an updated pyproject.toml
sync:
	@$(PIP) install -e .
	@echo "Environment updated with new dependencies."

# 3. Cleanup
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +