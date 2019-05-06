from event_manager.get_app import get_app

from event_manager.types.order import Order

from .queue import QUEUES

broker_url = 'amqp://rabbitmq:5672'

app = get_app('billing', broker_url, QUEUES)
