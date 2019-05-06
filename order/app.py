from celery import Celery
from event_manager.get_app import get_app
from kombu import Exchange, Queue

broker_url = 'amqp://rabbitmq:5672'
app = get_app('producer', broker_url, tuple())
