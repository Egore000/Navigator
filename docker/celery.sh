#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.backend.tasks._celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.backend.tasks._celery:celery flower
fi