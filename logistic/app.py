from event_manager.get_app import get_app
from .queue import QUEUES

broker_url = 'amqp://rabbitmq:5672'

app = get_app('logistic', broker_url, QUEUES)
