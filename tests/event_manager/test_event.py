from unittest import TestCase, main

import attr
import cattr

from kombu import Exchange
from celery import Task, Celery

from event_manager.event import Event


class TestEvent(TestCase):
    def setUp(self):
        @attr.s(auto_attribs=True)
        class Test:
            data: int
            event = Event(Exchange(), '')
        self.test_class = Test

    def test_class_access(self):
        """ Shows that it assigns the owner on access. """
        self.assertIs(self.test_class.event.owner, self.test_class)

    def test_init(self):
        """ Test the initialization. """
        exchange = Exchange()

        event = Event(exchange, 'test.task')

        # assignments
        self.assertIs(event.exchange, exchange)
        self.assertEqual(event.routing_key, 'test.task')

        # task creation.
        self.assertIsInstance(event.task, Task)
        self.assertEqual(event.task.name, 'test.task')


class TestRun(TestCase):
    """
    Test run cases
    """
    def test_register_and_run(self):
        """ Test the how the run works. """

        @attr.s(auto_attribs=True)
        class Test1:
            data: int
            event = Event(Exchange(), 'test_register_and_run')\


        @Test1.event.register_callback
        def callback(*args, **kwargs):
            return 'some return'

        self.assertIs(Test1.event.owner, Test1)

        app = Celery(task_always_eager=True)
        app.conf.update(CELERY_ALWAYS_EAGER=True)

        Test1.event.task.bind(app)

        task = Test1(1).event()
        task.get()

        # returns a dict of the function names and the function return value.
        self.assertEqual({'callback': 'some return'}, task.get())

    def test_no_owner(self):
        """ It raises an Attribute Error if the event has no owner. """

        app = Celery(task_always_eager=True)
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        event_ = Event(Exchange(), 'test_no_owner')

        @attr.s(auto_attribs=True)
        class Test2:
            data: int
            event = event_

        task = event_.task.delay(instance=cattr.unstructure(Test2(1)))

        with self.assertRaises(AttributeError):
            task.get()

    def test_no_register(self):
        """ It raises an Attribute Error if the event has no owner. """

        app = Celery(task_always_eager=True)
        app.conf.update(CELERY_ALWAYS_EAGER=True)

        @attr.s(auto_attribs=True)
        class Test3:
            data: int
            event = Event(Exchange(), 'test_no_register')

        task = Test3(1).event()

        self.assertEqual({}, task.get())


if __name__ == '__main__':
    main()
