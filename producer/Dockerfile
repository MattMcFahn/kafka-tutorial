FROM python:3.9.5 as python-base

# create non-root user
RUN addgroup --system --gid 1000 app \
 && adduser --system --gid 1000 --uid 1000 app --disabled-password --disabled-login

# create application space
RUN mkdir /app \
 && chown -R app:app /app \
 && chmod -R 770 /app

# TODO: We don't need this, just build a wheel and install
# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
#    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        # Specific dotenv dep
        python3-dotenv


# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -



# Not used
## copy entrypoint script and set permissions
#COPY ./entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
#
## set the entrypoint
#ENTRYPOINT [ "/entrypoint.sh" ]

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as python-build

# proxy settings for running in Jenkins and accessing the internet, default to nothing
ARG http_proxy=""
ARG https_proxy=""
ARG no_proxy=""

ENV http_proxy $http_proxy
ENV https_proxy $https_proxy
ENV no_proxy $no_proxy

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# proxy settings not needed at run time
ENV http_proxy ''
ENV https_proxy ''
ENV no_proxy ''



FROM python-build as python-app

WORKDIR $PYSETUP_PATH
COPY producer ./producer/
RUN poetry install --no-dev

RUN mkdir -p /app/logs \
 && chown -R app:app /app/logs \
 && chmod -R 770 /app/logs


CMD ["poetry", "run", "python", "-m", "producer"]
