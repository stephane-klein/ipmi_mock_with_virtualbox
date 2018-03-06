import os
import grpc
from concurrent import futures
import time

from . import ipmi_pb2
from . import ipmi_pb2_grpc

from . import ipmi

class IPMIServicer(ipmi_pb2_grpc.IPMIServicer):
    def On(self, request, context):
        response = ipmi_pb2.IPMIResponse()
        response.result = ipmi.on(request.ip)
        return response

    def Off(self, request, context):
        response = ipmi_pb2.IPMIResponse()
        response.result = ipmi.off(request.ip)
        return response

    def Cycle(self, request, context):
        response = ipmi_pb2.IPMIResponse()
        response.result = ipmi.cycle(request.ip)
        return response

    def Status(self, request, context):
        response = ipmi_pb2.IPMIResponse()
        response.result, response.msg = ipmi.status(request.ip)
        return response


def main():
    ipmi.load_config(os.environ.get('CONFIG_FILE', 'ipmi-config.json'))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ipmi_pb2_grpc.add_IPMIServicer_to_server(IPMIServicer(), server)

    SERVER_PORT = os.environ.get('PORT', 41000)

    print('Starting server. Listening on port 0.0.0.0:%s.' % SERVER_PORT)
    server.add_insecure_port('[::]:%s' % SERVER_PORT)
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
