from functools import partial
from typing import Callable, TypeVar, Type, Dict, Any

import cattr

from celery import shared_task, Task
from kombu import Exchange


Message = TypeVar('Message')


class Event:
    owner: Type[Message] = None

    def __init__(self, exchange: Exchange, routing_key: str):
        """ Create the tasks at initialization time. """
        self.exchange = exchange
        self.routing_key = routing_key
        self.__callbacks: Dict[str, Callable[[Message], None]] = {}
        self.task = self._get_task({
            'exchange': exchange,
            'routing_key': routing_key,
            'name': routing_key,
        })

    def __get__(self, instance: Message, owner: Type[Message]):
        """
        Set up the owner or initialize the task.
        Unfortunately the instance knows about its owner only
        from when the __get__ is called first.
        """
        if owner is not None:
            self.owner = owner
        elif instance:
            self.owner = instance.__class__

        if instance:
            # returns a partial that can be called whenever you want.
            return partial(
                self.task.delay,
                instance=cattr.unstructure(instance)
            )
        return self

    def _get_task(self, options: dict) -> Task:
        """
        This creates and returns a shared task.
        """
        def closure(*args, instance: Message, **kwargs) -> Dict[str, Any]:
            """
            This is the actual task, we need a closure so that
            ``self`` does not get serialized.
            """
            """
            The idea itself is that the ``self`` object that consume the task
            is not the same.
            """
            if self.owner:
                instance = cattr.structure(instance, self.owner)

                data = {}
                for name, callback in self.__callbacks.items():
                    data[name] = callback(instance, *args, **kwargs)
                return data

            else:
                raise AttributeError(
                    f'No owner registered! '
                    f'Probably no callback was registered for '
                    f'{self.routing_key}'
                )

        task = shared_task(**options)(closure)
        return task

    def register_callback(self, callback: Callable[[Message], Any]):
        """ This method allow to register a callback. """
        self.__callbacks[callback.__name__] = callback
        return callback
