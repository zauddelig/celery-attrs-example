from typing import Callable, List, ClassVar, Sequence
import attr
from event_manager.event import Event

from event_manager.exchanges import ORDER_EXCHANGE
from .order_line import OrderLine


@attr.s
class Order:
    id: int = attr.ib()
    lines: Sequence[OrderLine] = attr.ib(
        default=list)


    submit = Event(ORDER_EXCHANGE, 'order.v1.submit')
    refuse = Event(ORDER_EXCHANGE, 'order.v1.refuse')
