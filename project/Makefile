# Define the path to the virtual environment's python/pip 
VENV = .venv 
PYTHON = $(VENV)/bin/python3 
PIP = $(VENV)/bin/pip 

.PHONY: all install-deps install run debug lint clean 
# Setup virtual environment and dependencies 
install: $(VENV)/bin/activate install-deps 

$(VENV)/bin/activate: 
	@test -d $(VENV) || (echo "Creating .venv..." && python3 -m venv $(VENV)) 
 	.venv/bin/pip install --upgrade pip 
	@echo "Virtual environment ready." 
	
# Install dependencies and MiniLibX 
install-deps: 
	@echo "Installing Python dependencies..." 
	.venv/bin/pip install -e .[dev] 
	@echo "Installing MiniLibX..." 
	@chmod +x install_minilibx.sh 
	./install_minilibx.sh 
	@echo "Handshake complete. Dependencies are synced." 
	
# # Run the project 
#run: install 
# @$(PYTHON) -m amazeing 

# # Debug the project (using pdb) 
# debug: 
# @$(PYTHON) -m pdb -m amazeing 

# # Linting and type checking 
# lint: 
# @echo "Running flake8..." 
# @$(PYTHON) -m flake8 amazeing --max-line-length=88 
# @echo "Running mypy..." 
# @$(PYTHON) -m mypy amazeing --strict 

# Clean temporary files 
clean: 
	rm -rf $(VENV) 
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	find . -type d -name "*.egg-info" -exec rm -rf {} + 
	find . -type f -name "*.pyc" -delete 
	@echo "Clean complete."