import grpc
import hrm_pb2
import hrm_pb2_grpc
from google.protobuf.wrappers_pb2 import StringValue


with grpc.insecure_channel('localhost:50051') as channel:
    stub = hrm_pb2_grpc.PersonControllerStub(channel)
    request = hrm_pb2.PersonPartialUpdateRequest(id=1, name=StringValue(value="amy"))
    response = stub.PartialUpdate(request)
    print(response, end='')
