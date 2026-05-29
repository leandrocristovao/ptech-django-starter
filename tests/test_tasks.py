from app.tasks import add


def test_celery_task_can_be_called_directly():
    assert add(2, 3) == 5
