install:
	uv sync
start:
	uv run python manage.py runserver
check:
	uv run ruff check .
build:
	./build.sh
fix:
	uv run ruff check --fix
render-start:
	gunicorn task_manager.wsgi
make_migrations:
	uv run python manage.py makemigrations
migrate:
	uv run python manage.py migrate
collectstatic:
	uv run python manage.py collectstatic --noinput
make_mess:
	uv run django-admin makemessages -l ru
compile_mess:
	uv run django-admin compilemessages -l ru
test:
	uv run python manage.py test --keepdb

