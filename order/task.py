from order.app import app

from event_manager.types.order import Order, OrderLine

if __name__ == '__main__':
    order = Order(1, [
        OrderLine(1, 2, 3),
        OrderLine(2, 1, 4.5),
    ])
    # print(app.tasks)
    print('sending')
    tsk = order.submit()
    print('sent')
    # print(tsk)
    print('end')
    # print(tsk.get())
