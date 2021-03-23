from __future__ import print_function

import logging

import grpc

import user_pb2
import user_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = stub.SubmitData(user_pb2.UserDataRequest(name='Adrian', cnp='225200'))
    print("Client received: " + response.response)


if __name__ == '__main__':
    logging.basicConfig()
    run()
