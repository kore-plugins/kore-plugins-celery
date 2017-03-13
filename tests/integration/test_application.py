import pytest

from celery.app import shared_task
from celery.contrib.testing import tasks


class TestApplication(object):

    @pytest.fixture
    def task_func(self):
        def func(x, y):
            return x + y
        return func

    @pytest.fixture
    def task(self, task_func):
        return shared_task(task_func)

    def test_ping(self, application, application_worker):
        assert tasks.ping() == 'pong'

    def test_shared_task(
            self, application, application_worker, task, task_func):
        application.tasks.register(task)
        assert task_func(1, 2) == 3
