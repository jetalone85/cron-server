import threading

from grpc.grpc_server import GRPCServer

server = GRPCServer(port=8000)
server_thread = threading.Thread(target=server.start)
server_thread.start()

server_thread.join()
