WORKDIR = backend
PYTHON-VERSION = 3.9.11
PROJECT-NAME = foodgram
DOCKER_COMPOSE = docker compose -f infra/docker-compose.yml

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)
	pymarkdown scan .

admin:
	$(DOCKER_COMPOSE) exec backend python manage.py createsuperuser

migrations:
	$(DOCKER_COMPOSE) exec backend python manage.py makemigrations

up:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d --build
	$(DOCKER_COMPOSE) exec backend /app/entrypoint.sh

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs

env:
	pyenv local $(PYTHON-VERSION)
	pyenv virtualenv $(PYTHON-VERSION) $(PROJECT-NAME)
	pyenv local $(PROJECT-NAME)
	python -m pip install --upgrade pip
	pip install -r $(WORKDIR)/requirements.txt
