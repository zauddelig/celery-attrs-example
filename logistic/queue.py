from kombu import Queue

from event_manager.exchanges import ORDER_EXCHANGE


QUEUES = (
    Queue(f'logistic_order', exchange=ORDER_EXCHANGE,
          routing_key='order.*.submit'),
)