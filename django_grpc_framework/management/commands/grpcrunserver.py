# -*- coding: utf-8 -*-
from concurrent import futures

import grpc
from django.core.management.base import BaseCommand, CommandError

from django_grpc_framework.settings import grpc_settings


class Command(BaseCommand):
    help = 'Run gRPC server'

    def handle(self, *args, **options):
        self._serve()

    def _serve(self):
        self.stdout.write('Starting grpc server')
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_settings.ROOT_HANDLERS_HOOK(server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
