rm:
	docker-compose stop \
	&& docker-compose rm \
	&& rmdir /s /q pgdata/

up:
	docker-compose -f docker-compose.yaml up --force-recreate

alem:
	alembic upgrade head

fill:
	py seed.py

se:
	py DBselect.py