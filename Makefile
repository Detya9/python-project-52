install:
	uv sync
start:
	uv run python3 manage.py runserver
check:
	uv run ruff check .
build:
	./build.sh
fix:
	uv run ruff check --fix
render-start:
	gunicorn task_manager.wsgi
migrate:
	uv run manage.py migrate
collectstatic:
	uv run python manage.py collectstatic --noinput

