from socket import *


def SocketClient(method):
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('127.0.0.1', 25252))

    print('연결 확인 됐습니다.')
    clientSock.send(method.encode('utf-8'))

    print('메시지를 전송했습니다.')

    data = clientSock.recv(1024)
    data = data.decode('utf-8')
    print('받은 데이터 : ',data )
    return data