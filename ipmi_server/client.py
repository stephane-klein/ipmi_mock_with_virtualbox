#!/usr/bin/env python3
import os
import grpc
import argparse

import ipmi_pb2
import ipmi_pb2_grpc

channel = grpc.insecure_channel('%s:%s' % (
    os.environ.get('HOST', 'localhost'),
    os.environ.get('PORT', '50051')
))
stub = ipmi_pb2_grpc.IPMIStub(channel)

parser = argparse.ArgumentParser()
parser.add_argument("-I", dest="interface", type=str)
parser.add_argument("-H", dest="address", type=str, help="Remote server address, can be IP address or hostname. This option is required for lan and lanplus interfaces.")
parser.add_argument("-U", dest="user", type=str)
parser.add_argument("-P", dest="password", type=str)
subparsers = parser.add_subparsers(help='power help', dest='power')
parser_power = subparsers.add_parser('power', help='power help')

power_subparsers = parser_power.add_subparsers(dest='power')
parser_power_cycle = power_subparsers.add_parser('cycle', help='Provides a power off interval of at least 1 second.')
parser_power_on = power_subparsers.add_parser('on', help='Power up chassis')
parser_power_off = power_subparsers.add_parser('off', help='Power down chassis into soft off')

args = parser.parse_args()

if args.power == 'cycle':
    response = stub.Cycle(ipmi_pb2.IPMIRequest(ip=args.address))

elif args.power == 'on':
    response = stub.On(ipmi_pb2.IPMIRequest(ip=args.address))

elif args.power == 'off':
    response = stub.Off(ipmi_pb2.IPMIRequest(ip=args.address))

print("Result: %s" % response.result)
