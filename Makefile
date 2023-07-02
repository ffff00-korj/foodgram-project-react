WORKDIR = backend
PYTHON-VERSION = 3.9.11
PROJECT-NAME = foodgram
MANAGE = python $(WORKDIR)/manage.py

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)
	pymarkdown scan .

shell:
	$(MANAGE) shell

db:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

upnotest:
	$(MANAGE) runserver

test:
	pytest
	$(MANAGE) test $(WORKDIR) -v 2

up: test
	$(MANAGE) runserver

env:
	pyenv local $(PYTHON-VERSION)
	pyenv virtualenv $(PYTHON-VERSION) $(PROJECT-NAME)
	pyenv local $(PROJECT-NAME)
	python -m pip install --upgrade pip
	pip install -r requirements.txt
