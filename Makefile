.PHONY: clean

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py install

clean:
	rm -rf brain_mri_viewer/__pycache__
	rm -rf $(VENV)
