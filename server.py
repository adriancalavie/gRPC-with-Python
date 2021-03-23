import datetime
import logging
from concurrent import futures

import grpc

import user_pb2
import user_pb2_grpc


class Server(user_pb2_grpc.UserServicer):
    def SubmitData(self, request, context):
        age = get_age(request.cnp)
        gender = get_gender(request.cnp)
        print('Client ' + request.name + f"({gender}, {age} years)" + ' connected.')
        return user_pb2.ServerResponse(response="Submitted.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started')
    server.wait_for_termination()


def get_age(cnp):
    default_year = 1900
    today_date = datetime.date.today()

    gender = cnp[0]
    year = cnp[1:3]
    month = cnp[3:5]
    day = cnp[5:7]

    period_count = {
        1: default_year,
        2: default_year,
        5: default_year + 100,
        6: default_year + 100,
        7: default_year,
        8: default_year

    }

    client_birth_date = datetime.date(period_count.get(int(gender)) + int(year), int(month), int(day))

    return int((today_date - client_birth_date).days / 365)


def get_gender(cnp):
    gender = cnp[0]

    if int(gender) % 2 == 0:
        return "female"
    else:
        return "male"


if __name__ == '__main__':
    logging.basicConfig()
    serve()
