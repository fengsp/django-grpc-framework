from blog.services import PostService
from blog_proto import post_pb2_grpc


def grpc_handlers(server):
    post_pb2_grpc.add_PostControllerServicer_to_server(PostService.as_servicer(), server)
