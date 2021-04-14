docker-compose exec -T django-socio-grpc flake8 .
docker-compose exec -T django-socio-grpc black .
docker-compose exec -T django-socio-grpc isort --recursive .
