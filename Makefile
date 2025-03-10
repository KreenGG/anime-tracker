DC = docker compose

app:
	${DC} up --build

storages:
	${DC} up -d postgres

storages-test:
	${DC} -f docker-compose-test.yaml up -d

down:
	${DC} down

down-test:
	${DC} -f docker-compose-test.yaml down
