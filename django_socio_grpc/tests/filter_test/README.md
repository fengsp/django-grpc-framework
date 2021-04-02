command to compile proto file to python file:

```
docker-compose run django-socio-grpc python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./django_socio_grpc/tests/filter_test/filter_test.proto
```