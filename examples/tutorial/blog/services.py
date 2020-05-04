from blog_proto import post_pb2
from blog.models import Post
from blog.serializers import PostSerializer
from django_grpc_framework import mixins
from django_grpc_framework import generics


"""
class PostService(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericService):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    protobuf_class = post_pb2.Post
"""


class PostService(generics.ModelService):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    protobuf_class = post_pb2.Post
