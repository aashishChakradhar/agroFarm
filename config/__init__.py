# config/__init__.py
from __future__ import absolute_import, unicode_literals

# Import celery
from .celery import app as celery_app

# Export celery app
__all__ = ['celery_app']