from __future__ import print_function

import logging

import grpc

import user_pb2
import user_pb2_grpc


# def run():
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = user_pb2_grpc.UserStub(channel)
#
#         response = stub.SubmitData(user_pb2.UserDataRequest(name='Adrian', cnp='225200'))
#     print("Client received: " + response.response)


class Client(object):
    __whatever = 12

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = user_pb2_grpc.UserStub(self.channel)

        self.name = input('Enter a name: ')
        self.cnp = input('Enter a TIN: ')

    def submit(self):
        response = self.stub.SubmitData(user_pb2.UserDataRequest(name=self.name, cnp=self.cnp))
        return response


def run():
    client = Client()

    is_connected = True

    while is_connected:
        option = input('Enter option: ')

        if option is '1':
            print('Sending data...')
            print(str(client.submit()))

        elif option is '2':
            print('Ended connection')
            is_connected = False

        else:
            print('Invalid option. Choose again!')


if __name__ == '__main__':
    logging.basicConfig()
    run()
