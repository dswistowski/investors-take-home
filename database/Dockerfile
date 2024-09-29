FROM python:3.12-slim AS build

RUN apt-get update
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.in-project true

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --only main

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=build /app /app/
COPY . /app/

ENV PATH="/app/.venv/bin:$PATH"
CMD [ "python", "-m", "seed" ]
