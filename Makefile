build:
	docker compose -f local.yml up --build -d --remove-orphans

down:
	docker compose -f local.yml down -v

sdown:
	docker compose -f staging.yml down -v

mk:
	docker compose -f local.yml run --rm api python manage.py makemigrations

mt:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

