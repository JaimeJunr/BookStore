# Etapa base para o Python e dependências do sistema
FROM python:3.9-slim as python-base

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instala as dependências do sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN pip install poetry

# Etapa de dependências
FROM python-base as builder

# Define o diretório para o setup das dependências
WORKDIR $PYSETUP_PATH

# Copia os arquivos de gerenciamento de dependências
COPY pyproject.toml poetry.lock ./

# Instala dependências de produção (sem pacotes de desenvolvimento)
RUN poetry install --no-dev

# Etapa final: produção
FROM python-base as production

# Copia o ambiente virtual da etapa anterior
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

# Define o diretório de trabalho da aplicação
WORKDIR /app

# Copia o código da aplicação
COPY . .

# Exponha a porta do Django
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
