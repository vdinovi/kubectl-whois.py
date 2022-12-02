import typing
import json
import abc

OUTPUT_FORMATS: typing.List[str] = ["json"]
OUTPUT_FORMAT_DEFAULT: str = "json"

# TODO: explore replacing ABC with typing.Protocol


class AbstractFormatter(abc.ABC):
    @abc.abstractmethod
    def format(self, data: str) -> str:
        ...


class JsonFormatter(AbstractFormatter):
    def format(self, data: str) -> str:
        return json.dumps()


class Output:
    def __init__(self, formatter: typing.Optional[AbstractFormatter] = None) -> None:
        if not formatter:
            self._formatter = JsonFormatter()
        else:
            self._formatter = formatter
