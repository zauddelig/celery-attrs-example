from event_manager.types.order import Order


@Order.submit.register_callback
def billing_received(order: Order):
    print(f'billing received a task for order {order}')
