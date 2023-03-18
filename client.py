import argparse
import xmlrpc.client


class Command:
    def __init__(self, name, help_msg):
        self.name = name
        self.help_msg = help_msg

    def add_arguments(self, parser):
        pass

    def run(self, args, server):
        pass


class PowCommand(Command):
    def __init__(self):
        super().__init__("pow", "Calculate a power")

    def add_arguments(self, parser):
        parser.add_argument("base", type=int, help="The base")
        parser.add_argument("exp", type=int, help="The exponent")

    def run(self, args, server):
        result = server.math.pow(args.base, args.exp)
        print(f"Result: {result}")


class AddCommand(Command):
    def __init__(self):
        super().__init__("add", "Add two numbers")

    def add_arguments(self, parser):
        parser.add_argument("x", type=int, help="The first number")
        parser.add_argument("y", type=int, help="The second number")

    def run(self, args, server):
        result = server.math.add(args.x, args.y)
        print(f"Result: {result}")


class CLI:
    def __init__(self):
        self.commands = [
            PowCommand(),
            AddCommand(),
        ]
        self.server = xmlrpc.client.ServerProxy("http://localhost:8000")

    def run(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        for command in self.commands:
            cmd_parser = subparsers.add_parser(command.name, help=command.help_msg)
            command.add_arguments(cmd_parser)

        args = parser.parse_args()

        for command in self.commands:
            if command.name == args.command:
                command.run(args, self.server)
                break
        else:
            print("Error: Invalid command.")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
