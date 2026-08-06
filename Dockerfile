FROM python:3.14
LABEL authors="KuprinaSA"

WORKDIR /code

RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock ./

#заставляет Poetry использовать текущую среду Python и устанавливает poetry. Можно указать --only main что бы он не устанавливал литеры зависимости flake8...
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --only main

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]