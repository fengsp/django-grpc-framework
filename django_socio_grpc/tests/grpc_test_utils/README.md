command to compile proto file to python file:

```
docker-compose run django-socio-grpc python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./django_socio_grpc/tests/grpc_test_utils/unittest.proto
# or if docker already run 
docker-compose exec django-socio-grpc python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./django_socio_grpc/tests/grpc_test_utils/unittest.proto
```