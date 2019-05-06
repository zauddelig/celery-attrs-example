from celery import Celery



def get_app(name, url, queues):
    app = Celery(name, broker=url, backend=url)
    app.conf.task_queues = queues
    return app
