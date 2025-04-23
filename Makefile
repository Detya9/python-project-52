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
migrate:
	uv run manage.py migrate
collectstatic:
	uv run python manage.py collectstatic --noinput
make_mess:
	uv run django-admin makemessages -l ru
compile_mess:
	uv run django-admin compilemessages -l ru
test:
	uv run python manage.py test --keepdb

