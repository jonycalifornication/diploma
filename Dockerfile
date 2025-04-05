# Базовый образ Python с uv
FROM python:3.12-slim-bookworm

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем curl и сертификаты для загрузки uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Скачиваем и устанавливаем uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Обновляем PATH для uv
ENV PATH="/root/.local/bin/:$PATH"

ENV PYTHONPATH="/app"
# Копируем файлы проекта и зависимостей
COPY ./pyproject.toml ./uv.lock ./entrypoint.sh ./

# Устанавливаем зависимости через uv
RUN uv sync --frozen

RUN uv add pydantic-settings
# Копируем код бота
COPY src ./src

# Делаем entrypoint.sh исполняемым
RUN chmod +x entrypoint.sh