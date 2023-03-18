import threading
import unittest
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


class GRPCServer:
    def __init__(self, port: int = 8000):
        self.port = port
        self.server = None
        self.server_thread = None

    def start(self):
        with SimpleXMLRPCServer(("localhost", self.port), requestHandler=RequestHandler) as server:
            self.server = server
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

    def start_server_thread(self):
        self.server_thread = threading.Thread(target=self.start)
        self.server_thread.start()

    def stop_server_thread(self):
        self.server.shutdown()


class TestGRPCServer(unittest.TestCase):
    def setUp(self):
        self.server = GRPCServer(port=8000)
        self.server.start_server_thread()

    def tearDown(self):
        self.server.stop_server_thread()
        self.server.server_thread.join()

    def test_pow(self):
        proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
        result = proxy.math.pow(2, 3)
        self.assertEqual(result, 8)

    def test_add(self):
        proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
        result = proxy.math.add(2, 3)
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
