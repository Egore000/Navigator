FROM python:3.12.3

RUN mkdir /navigator

WORKDIR /navigator

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /navigator/docker/*.sh

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]