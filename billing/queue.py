from kombu import Queue

from event_manager.exchanges import ORDER_EXCHANGE


QUEUES = (
    Queue(f'billing_order', exchange=ORDER_EXCHANGE,
          routing_key='order.*.submit'),
)
