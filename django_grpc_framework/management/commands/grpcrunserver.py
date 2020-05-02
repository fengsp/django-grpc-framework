# -*- coding: utf-8 -*-
from concurrent import futures

import grpc
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run gRPC server'

    def handle(self, *args, **options):
        self._serve()

    def _serve(self):
        self.stdout.write('Starting grpc server')
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        root_grpc_handlers_conf = '%s.grpc_handlers' % settings.ROOT_URLCONF
        grpc_handlers = import_string(root_grpc_handlers_conf)
        grpc_handlers(server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
