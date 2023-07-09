WORKDIR = backend
PYTHON-VERSION = 3.9.11
PROJECT-NAME = foodgram
MANAGE = python $(WORKDIR)/manage.py
DOCKER_COMPOSE = infra/docker-compose.yml

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)
	pymarkdown scan .

admin:
	$(MANAGE) createsuperuser

db:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

up:
	docker compose -f $(DOCKER_COMPOSE) up

test:
	pytest backend/

env:
	pyenv local $(PYTHON-VERSION)
	pyenv virtualenv $(PYTHON-VERSION) $(PROJECT-NAME)
	pyenv local $(PROJECT-NAME)
	python -m pip install --upgrade pip
	pip install -r requirements.txt
