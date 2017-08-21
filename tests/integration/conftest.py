import pytest

from celery import Celery
from celery.contrib.testing.manager import Manager
from celery.contrib.testing import worker

from kore import config_factory, container_factory


@pytest.fixture(scope='session')
def celery_config():
    return {
        'main': 'test',
        'broker_url': 'memory://',
        'result_backend': 'cache+memory://',
        'worker_hijack_root_logger': True,
    }


@pytest.fixture(scope='session')
def config(celery_config):
    return config_factory.create('dict', celery=celery_config)


@pytest.fixture
def celery_app():
    return Celery()


@pytest.fixture
def container(config, celery_app):
    initial = {
        'config': config,
        'kore.components.celery.application': celery_app,
    }
    return container_factory.create(**initial)


@pytest.fixture
def application(container):
    return container('kore.components.celery.application')


@pytest.fixture
def manager(application):
    return Manager(application)


@pytest.fixture()
def application_worker(request, application, celery_includes,
                       celery_worker_pool, celery_worker_parameters):
    # type: (Any, Celery, Sequence[str], str) -> WorkController
    """Fixture: Start worker in a thread, stop it when the test returns."""
    for module in celery_includes:
        application.loader.import_task_module(module)
    with worker.start_worker(application,
                             pool=celery_worker_pool,
                             **celery_worker_parameters) as w:
        yield w


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'celery.contrib.testing.tasks',
    ]
