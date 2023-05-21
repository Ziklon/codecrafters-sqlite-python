import abc

from abc import abstractmethod
from pathlib import Path
from typing import MutableMapping, Type

available_commands: MutableMapping[str, Type["Command"]] = {}

class InvalidCommand(Exception):
    """InvalidCommand"""

class CommandParseError(Exception):
    """CommandParseError"""

class CommandParser:
    MIN_ARGV_LENGTH = 2
    def __init__(self,argv):
        #print("init argv", argv, self.MIN_ARGV_LENGTH, len(argv))
        if len(argv) < self.MIN_ARGV_LENGTH:
            raise CommandParseError(f"Expected %d arguments got {argv}" % self.MIN_ARGV_LENGTH)
        self._database_file_path = Path(argv[1]).resolve().absolute()
        self._command = argv[2]
        if not self._database_file_path.is_file():
            raise CommandParseError(f"File not found: {self._database_file_path}")
    @property
    def database(self):
        return self._database_file_path

    @property
    def command(self):
        return self._command

    def has_valid_command(self):
        return Command.parse(self.command)
    
class Command(abc.ABC):
    command_str: str = None

    def __init__(self, *, database: Path):
        self._database = database
    
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        available_commands[cls.command_str] = cls
    
    def execute(self):
        return self._execute_impl()

    @abstractmethod
    def _execute_impl(self):
        ...
    
    @classmethod
    def from_parser(cls, val: CommandParser):
        cmd = val.command
        if not cls.parse(cmd):
            raise InvalidCommand(cmd)
        command_cls = available_commands.get(cmd)
        return command_cls(database=val.database)
    
    @classmethod
    def parse(cls, val: str):
        return val in available_commands.keys()
    
class NullCommand(Command):
    command_str = ""
    def __init__(self, **kwargs):
        pass
    
    def _execute_impl(self):
        pass
    

class CommandRunner:
    
    def __init__(self, *, parser: CommandParser) -> None:
        self._parser = parser
        self._command: Command = NullCommand()

        if not parser.has_valid_command():
            print(f"Invalid commands : {parser.command}")
        
    @property
    def command(self):
        if isinstance(self._command, NullCommand):
            self._command = Command.from_parser(self._parser)
        return self._command

    def run(self):
        self.command.execute()