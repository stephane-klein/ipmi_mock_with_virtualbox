import os
import grpc
import argparse

from . import ipmi_pb2
from . import ipmi_pb2_grpc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", dest="interface", type=str)
    parser.add_argument("-H", dest="address", type=str, help="Remote server address, can be IP address or hostname. This option is required for lan and lanplus interfaces.")
    parser.add_argument("-U", dest="user", type=str)
    parser.add_argument("-P", dest="password", type=str)
    parser.add_argument("-p", dest="port", default="41000", type=str)
    subparsers = parser.add_subparsers(help='power help', dest='power')
    parser_power = subparsers.add_parser('power', help='power help')

    power_subparsers = parser_power.add_subparsers(dest='power')
    parser_power_cycle = power_subparsers.add_parser('cycle', help='Provides a power off interval of at least 1 second.')
    parser_power_on = power_subparsers.add_parser('on', help='Power up chassis')
    parser_power_off = power_subparsers.add_parser('off', help='Power down chassis into soft off')
    parser_power_status = power_subparsers.add_parser('status', help='Show current chassis power status')

    args = parser.parse_args()

    channel = grpc.insecure_channel(os.environ.get('IPMI_MOCK_SERVER', 'localhost'))
    stub = ipmi_pb2_grpc.IPMIStub(channel)

    if args.power == 'cycle':
        response = stub.Cycle(ipmi_pb2.IPMIRequest(ip=args.address))
        print("Result: %s" % response.result)

    elif args.power == 'on':
        response = stub.On(ipmi_pb2.IPMIRequest(ip=args.address))
        print("Result: %s" % response.result)

    elif args.power == 'off':
        response = stub.Off(ipmi_pb2.IPMIRequest(ip=args.address))
        print("Result: %s" % response.result)

    elif args.power == 'status':
        response = stub.Status(ipmi_pb2.IPMIRequest(ip=args.address))
        print(
            "Chassis Power is %s" %
            (
                'on' if response.msg == 'running' else 'off'
            )
        )
