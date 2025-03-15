DC = docker compose
MAIN_APP_CONTAINER_NAME= anime-tracker-main-app

run:
	${DC} up -d

stop:
	${DC} down

migrations:
	docker exec -it ${MAIN_APP_CONTAINER_NAME} alembic upgrade head

# make revision --text="your text"
revision:
	docker exec -it ${MAIN_APP_CONTAINER_NAME} alembic revision --autogenerate -m "$(text)"

# Tests
test-db:
	${DC} -f docker-compose-test.yaml up -d

test-db-down:
	${DC} -f docker-compose-test.yaml down
