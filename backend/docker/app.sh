#!/bin/bash

alembic revision --autogenerate -m 'all migrations 1'

alembic upgrade head

gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000