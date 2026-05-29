"""Celery tasks for the main app."""

from celery import shared_task


@shared_task(name="app.add")
def add(x: int, y: int) -> int:
    return x + y
