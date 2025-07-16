

.ONESHELL:
venv:
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip setuptools wheel pipenv
	./venv/bin/python -m pip install -e .

# transform
.PHONY: transform
transform:
	message transform

# get_message
.PHONY: get_message
get_message:
	message get-message "$(SESSION_GROUP)"