DC = docker compose

run:
	${DC} up -d

down:
	${DC} down

# Tests
test-db:
	${DC} -f docker-compose-test.yaml up -d

test-db-down:
	${DC} -f docker-compose-test.yaml down
