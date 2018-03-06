import os
import grpc
from concurrent import futures
import time

import ipmi_pb2
import ipmi_pb2_grpc

import ipmi

ipmi.load_config(os.environ.get('CONFIG_FILE', 'ipmi-config.json'))

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


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ipmi_pb2_grpc.add_IPMIServicer_to_server(IPMIServicer(), server)

SERVER_PORT = os.environ.get('PORT', 50051)

print('Starting server. Listening on port %s.' % SERVER_PORT)
server.add_insecure_port('[::]:%s' % SERVER_PORT)
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
