
from event_manager.types.order import Order


@Order.submit.register_callback
def logistic_received(order: Order):
    print(f'logistic received the order {order}')
