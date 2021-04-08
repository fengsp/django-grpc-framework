import grpc

from blog.models import Post
from blog_proto import post_pb2, post_pb2_grpc
from django_socio_grpc.test import RPCTestCase


class PostServiceTest(RPCTestCase):
    def test_create_post(self):
        stub = post_pb2_grpc.PostControllerStub(self.channel)
        response = stub.Create(post_pb2.Post(title="title", content="content"))
        self.assertEqual(response.title, "title")
        self.assertEqual(response.content, "content")
        self.assertEqual(Post.objects.count(), 1)

    def test_list_posts(self):
        Post.objects.create(title="title1", content="content1")
        Post.objects.create(title="title2", content="content2")
        stub = post_pb2_grpc.PostControllerStub(self.channel)
        post_list = list(stub.List(post_pb2.PostListRequest()))
        self.assertEqual(len(post_list), 2)
