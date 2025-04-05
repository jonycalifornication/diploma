run: # run container apps
	docker compose -f docker-compose.yml up --build --abort-on-container-exit

run_dev:
	docker compose up
test: # run tests
	docker compose -f docker-compose-test.yml up --build --abort-on-container-exit --exit-code-from test_app

lint: # run pre-commit hooks
	uv run pre-commit run --all-files
