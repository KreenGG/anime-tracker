DC = docker compose

run:
	${DC} up -d

down:
	${DC} down

migrations:
	docker exec -it anime-tracker-main-app alembic upgrade head

# Tests
test-db:
	${DC} -f docker-compose-test.yaml up -d

test-db-down:
	${DC} -f docker-compose-test.yaml down
