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

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = user_pb2_grpc.UserStub(self.channel)

        self.name = input('Enter a name: ')

        is_cnp = False

        while not is_cnp:
            self.cnp = input('Enter a TIN:')

            if validate(self.cnp):
                is_cnp = True
                print('Connected.')
            else:
                print('Invalid TIN')

    def submit(self):
        response = self.stub.SubmitData(user_pb2.UserDataRequest(name=self.name, cnp=self.cnp))
        return response


def run():
    client = Client()

    is_connected = True

    options = {
        1: "1.Send data to the server",
        2: "2.Disconnect",
    }

    while is_connected:
        for index in options:
            print(options[index])

        option = input('Enter option: ')

        if option is '1':
            print('Sending data...')
            print(str(client.submit()))

        elif option is '2':
            print('Ended connection')
            is_connected = False

        else:
            print('Invalid option. Choose again!')


def validate(cnp):
    CNP_CONSTANT = "279146358279"
    component = 0

    birth_century = frozenset([1, 2, 5, 6, 7, 8])

    if len(cnp) != 13:
        return False
    elif cnp.isnumeric():
        gender = cnp[0]
        year = cnp[1:3]
        month = cnp[3:5]
        day = cnp[5:7]

        if int(gender) not in birth_century:
            return False

        if 1 > int(month) > 12:
            return False

        if 1 > int(day) > 31:
            return False

        for index in range(len(CNP_CONSTANT)):
            component += int(CNP_CONSTANT[index]) * int(cnp[index])

        remainder = component % 11

        if remainder == 10:
            remainder = 1

        if str(remainder).__eq__(cnp[-1]):
            return True
        else:
            return False

    return False


if __name__ == '__main__':
    logging.basicConfig()
    run()
