from blog.models import Post
from blog.serializers import PostProtoSerializer
from django_socio_grpc import generics, mixins


"""
class PostService(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericService):
    queryset = Post.objects.all()
    serializer_class = PostProtoSerializer
"""


class PostService(generics.ModelService):
    queryset = Post.objects.all()
    serializer_class = PostProtoSerializer
