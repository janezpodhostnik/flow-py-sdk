import logging
from abc import abstractmethod, ABCMeta

from examples.common.config import Config

log = logging.getLogger(__name__)


class _ExampleRegistry(object):
    def __init__(self):
        self._examples: dict[str, "Example"] = {}

    def register(self, ex: "Example"):
        """Register a new example

        There should be no need to call this explicitly,
        as the examples should be registered by inheriting the Example class

        Parameters
        ----------
        ex : Example
            The example to register

        """
        if ex.tag in self._examples:
            log.error(f"Trying to register an example with a duplicate tag: {ex.tag}")
            return
        self._examples[ex.tag] = ex

    async def run_all(self, cfg: Config):
        """Run all of the registered examples

        Parameters
        ----------
        cfg : Config
            Environment configuration for the examples
        """
        examples = sorted(self._examples.values(), key=lambda e: e.sort_order)
        for ex in examples:
            # noinspection PyBroadException
            log.info(f"=== RUNNING: [{ex.tag}] {ex.name} ===")
            try:
                await ex.run(cfg)
            except Exception:
                log.error(
                    "==== PASSED ====\n",
                    exc_info=True,
                    stack_info=True,
                )
                continue
            log.info("==== PASSED ====\n")


example_registry: _ExampleRegistry = _ExampleRegistry()


class _ExampleMetaClass(ABCMeta):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if cls.__name__ != "Example":
            example_registry.register(cls())


class Example(metaclass=_ExampleMetaClass):
    """Base class for examples

    Examples inheriting from this base class will automatically be registered to the example_registry
    and will be run with the other examples.

    ...

    Attributes
    ----------
    tag : str
        a short unique tag to identify the example
    name : str
        a descriptive name for the example
    sort_order : int
        a value to sort the test by when running multiple test at the same time
    """

    def __init__(self, *, tag: str, name: str, sort_order: int) -> None:
        """Constructs an example

        Example will be registered to the example_registry and will be run with the other examples.

        ...

        Parameters
        ----------
        tag : str
            a short unique tag to identify the example
        name : str
            a descriptive name for the example
        sort_order : int
            a value to sort the test by when running multiple test at the same time
        """

        super().__init__()
        self.sort_order = sort_order
        self.tag = tag
        self.name = name

    @abstractmethod
    async def run(self, ctx: Config):
        pass


def example(cls, *args, **kwargs):
    example_registry.register(cls(*args, **kwargs))
    return cls
