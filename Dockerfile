FROM python:3.11.6-alpine3.18
LABEL maintainer="oleksandr.hontarenko.dev@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

RUN python manage.py migrate && \
    python manage.py loaddata fixtures_db.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
