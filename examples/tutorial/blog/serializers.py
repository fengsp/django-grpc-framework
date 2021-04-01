from django_socio_grpc import proto_serializers
from blog.models import Post
from blog_proto import post_pb2


class PostProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Post
        proto_class = post_pb2.Post
        fields = ["id", "title", "content"]
