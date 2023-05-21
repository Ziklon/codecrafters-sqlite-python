import importlib
import pkgutil
import sys
from app.command import CommandParser, CommandRunner

for command in ("db_info", "tables"):
    module_name = f"app.commands.{command}"
    module = importlib.import_module(module_name)


def main(args):
    parser = CommandParser(args)
    runner = CommandRunner(parser=parser)
    runner.run()


if __name__ == "__main__":
    main(sys.argv)