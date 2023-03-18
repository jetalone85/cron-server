import threading
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


class GRPCServer:
    def __init__(self, port: int = 8000):
        self.port = port

    def start(self):
        with SimpleXMLRPCServer(("localhost", self.port), requestHandler=RequestHandler) as server:
            server.register_introspection_functions()

            def xmlrpc(name=None):
                def register_func(func):
                    def wrapper(*args, **kwargs):
                        try:
                            # Call the function and store the result in the database
                            result = func(*args, **kwargs)
                        except Exception as e:
                            # Handle exceptions and log the error
                            server.logger.error(f"Error while executing function {func.__name__}: {e}")
                            raise

                        return result

                    server.register_function(wrapper, name)
                    return wrapper

                return register_func

            @xmlrpc(name="math.pow")
            def pow(base: int, exp: int) -> int:
                return base ** exp

            @xmlrpc(name="math.add")
            def add(x: int, y: int) -> int:
                return x + y

            try:
                print("Starting XML-RPC server...")
                server.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down XML-RPC server...")
                server.shutdown()
                print("Server shutdown complete.")


server = GRPCServer(port=8000)
server_thread = threading.Thread(target=server.start)
server_thread.start()

server_thread.join()
