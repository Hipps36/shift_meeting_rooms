FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
