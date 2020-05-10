from blog.handlers import grpc_handlers as blog_grpc_handlers


urlpatterns = []


def grpc_handlers(server):
    blog_grpc_handlers(server)
