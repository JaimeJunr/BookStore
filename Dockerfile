# Base da imagem com Python 3.8.1
FROM python:3.9-slim as python-base


# Variáveis de ambiente
# Evita o buffering de saída do Python
ENV PYTHONUNBUFFERED=1 \
    # Impede a criação de arquivos .pyc
    PYTHONDONTWRITEBYTECODE=1 \
    # Permite o uso de cache do pip
    PIP_NO_CACHE_DIR=off \
    # Desativa a verificação de versão do pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # Define um timeout padrão para o pip
    PIP_DEFAULT_TIMEOUT=100 \
    # Define o diretório de instalação do Poetry
    POETRY_HOME="/opt/poetry" \
    # Cria o ambiente virtual no diretório do projeto
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # Desativa perguntas interativas durante a instalação
    POETRY_NO_INTERACTION=1 \
    # Define o caminho onde os requisitos e o ambiente virtual serão armazenados
    PYSETUP_PATH="/opt/pysetup" \
    # Define o caminho do ambiente virtual
    VENV_PATH="/opt/pysetup/.venv"

# Adiciona o Poetry e o ambiente virtual ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# Instala dependências do sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev gcc \
    && pip install psycopg2 \
    && pip install poetry poetry init \
    # Limpa o cache do apt-get para reduzir o tamanho da imagem
    && apt-get clean \
    # Remove listas de pacotes para economizar espaço
    && rm -rf /var/lib/apt/lists/**

# Define o diretório de trabalho para a instalação de dependências
WORKDIR $PYSETUP_PATH

# Copia os arquivos de gerenciamento de dependências
COPY poetry.lock pyproject.toml ./

# Instala dependências do projeto sem pacotes de desenvolvimento
RUN poetry install --no-dev


RUN python -m django --version


WORKDIR /app

# Copia o restante do código da aplicação
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
