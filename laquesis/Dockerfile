FROM python:3.11-slim

WORKDIR /app/laquesis

COPY . .

RUN pip install --upgrade pip && pip install pipenv

RUN pipenv install --deploy --system

CMD ["python", "src/main.py"]

