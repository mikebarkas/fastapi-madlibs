.PHONY: up down locust-1 locust-2 locust-docker-1 locust-docker-2

# ---------------------------------------------------------
# Docker
up:
	docker-compose up -d

down:
	docker-compose down

# ---------------------------------------------------------
# Locust testing
locust-1:
	locust --headless --users 10 --spawn-rate 3 --run-time 15s -H http://127.0.0.1:8000/v1

locust-2:
	locust --headless --users 10 --spawn-rate 3 --run-time 15s -H http://127.0.0.1:8000/v2

# ---------------------------------------------------------
# Docker endpoint :8002
locust-docker-1:
	locust --headless --users 10 --spawn-rate 3 --run-time 15s -H http://127.0.0.1:8002/v1

locust-docker-2:
	locust --headless --users 10 --spawn-rate 3 --run-time 15s -H http://127.0.0.1:8002/v2
