makemigrations:
	docker compose exec django_api python manage.py makemigrations

migrate:
	./wait-for-it.sh 127.0.0.1:8000	
	docker compose exec django_api python manage.py migrate

create_supperuser:
	docker compose exec django_api python3 manage.py shell -c "from django.contrib.auth.models import User; \
								User.objects.filter(username='admin').exists() or \
								User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

export_db:
	docker compose exec postgres pg_dump \
		--verbose --clean \
		--no-owner --no-privileges \
		--format=c \
		-c -U root -d omni_hr_db > dumped_db/dump.sql

create-new-db:
	docker compose down
	docker compose up postgres -d
	echo "waiting database really up"
	sleep 15
	docker compose exec postgres createdb -U root root || :
	docker compose exec postgres psql -U root --command='DROP DATABASE IF EXISTS omni_hr_db'
	docker compose exec postgres createdb -U root omni_hr_db || :

import-db:
	docker compose exec -T postgres pg_restore --no-owner --no-privileges \
  		--verbose --clean --format=c -U root -d omni_hr_db < dumped_db/dump.sql ||:

create_sample_data:
	docker compose up -d
	docker compose exec django_api python3 manage.py create_sample_data

build:
	docker compose build

up-all:
	docker compose up -d

collectstatic:
	docker compose exec django_api python manage.py collectstatic --noinput

setup-new-project: build create-new-db import-db up-all collectstatic

test-django-api:
	docker compose exec django_api python3 manage.py test --settings=main.settings.test --verbosity=1

test-django-api-debugpy:
	docker compose exec django_api bash -c "\
		python -m debugpy --listen 0.0.0.0:6678 --wait-for-client \
			manage.py test \
			--settings=main.settings.test \
			--verbosity=1 \
		"

test-fastapi:
	docker compose exec postgres psql -U root --command='DROP DATABASE IF EXISTS test_db'
	docker compose exec postgres createdb -U root test_db || :
	docker compose exec fast_api pytest -vv --capture=no

test-fastapi-debugpy:
	docker compose exec postgres psql -U root --command='DROP DATABASE IF EXISTS test_db'
	docker compose exec postgres createdb -U root test_db || :
	docker compose exec fast_api bash -c "python -m debugpy --listen 0.0.0.0:5679 --wait-for-client -m pytest -vv --capture=no"
