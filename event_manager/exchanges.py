from kombu import Exchange

ORDER_EXCHANGE = Exchange('order', type='topic')
