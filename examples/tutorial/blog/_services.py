import grpc
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf import empty_pb2
from django_grpc_framework.services import Service
from blog_proto import post_pb2
from blog.models import Post
from blog.serializers import PostSerializer


class PostService(Service):
    def List(self, request, context):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        for post_data in serializer.data:
            yield ParseDict(post_data, post_pb2.Post())

    def Create(self, request, context):
        data = MessageToDict(request, including_default_value_fields=True)
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ParseDict(serializer.data, post_pb2.Post())

    def get_object(self, pk, context):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

    def Retrieve(self, request, context):
        post = self.get_object(request.id, context)
        serializer = PostSerializer(post)
        return ParseDict(serializer.data, post_pb2.Post())

    def Update(self, request, context):
        post = self.get_object(request.id, context)
        data = MessageToDict(request, including_default_value_fields=True)
        serializer = PostSerializer(post, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ParseDict(serializer.data, post_pb2.Post())

    def Destroy(self, request, context):
        post = self.get_object(request.id, context)
        post.delete()
        return empty_pb2.Empty()
