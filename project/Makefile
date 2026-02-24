# Define the path to the virtual environment's python/pip 
VENV = .venv
PYTHON = $(VENV)/bin/python3 
PIP := $(VENV)/bin/pip 

.PHONY: all install-deps install run debug lint clean re
# Setup virtual environment and dependencies 
install: $(VENV)/bin/activate install-deps 

$(VENV)/bin/activate: 
	@test -d $(VENV) || (echo "Creating .venv..." && python3 -m venv $(VENV)) 
	@test -f $(VENV)/bin/pip || $(VENV)/bin/python -m ensurepip
	@test -f $(VENV)/bin/pip || ln -s $(VENV)/bin/pip3 $(VENV)/bin/pip
	$(VENV)/bin/pip install --upgrade pip 
	@touch $(VENV)/bin/activate
	@echo "Virtual environment ready." 
	
# Install dependencies and MiniLibX 
install-deps: 
	@echo "Installing Python dependencies..." 
	.venv/bin/pip install -e .[dev] 
	@echo "Installing modules..." 
	@chmod +x install_modules.sh 
	./install_modules.sh 
	@echo "Handshake complete. Dependencies are synced." 
	
# # Run the project 
run:
	@$(PYTHON) -m a_maze_ing config.txt

# # Debug the project (using pdb) 
debug: 
	@$(PYTHON) -m pdb -m a_maze_ing.py config.txt 

# # Linting and type checking 
lint-mypy: 
	@echo "Running mypy..." 
	@$(PYTHON) -m mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true
	@$(PYTHON) -m mypy modules/mazegen --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true

lint-flake:
	@echo "Running flake8..." 
	@$(PYTHON) -m flake8 src --max-line-length=79 || true
	@$(PYTHON) -m flake8 modules/mazegen --max-line-length=79 || true

lint: lint-mypy lint-flake

# Clean temporary files 
clean: 
	rm -rf $(VENV)
	rm -f modules/mazegen-1.0.tar.gz
	rm -rf modules/mazegen
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	find . -type d -name "*.egg-info" -exec rm -rf {} + 
	find . -type f -name "*.pyc" -delete 
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "map_output.txt" -exec rm -f {} +
	@echo "Clean complete."

re:
	make clean
	make
