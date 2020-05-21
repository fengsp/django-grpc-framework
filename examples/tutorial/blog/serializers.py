from django_grpc_framework import serializers
from blog.models import Post
from blog_proto import post_pb2


class PostProtoSerializer(serializers.ModelProtoSerializer):
    class Meta:
        model = Post
        proto_class = post_pb2.Post
        fields = ['id', 'title', 'content']
