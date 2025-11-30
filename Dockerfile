FROM python:3.14-slim AS base

ARG PORT=8089
ARG APP_NAME=app
ARG APP_PATH=/app

ARG VIRTUAL_ENV=/opt/venv

ENV \
  LC_CTYPE=UTF-8 \
  LANG=en_US.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONFAULTHANDLER=1

ENV \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_TOOL_BIN_DIR=/usr/local/bin \
  VIRTUAL_ENV=$VIRTUAL_ENV \
  PATH="$VIRTUAL_ENV/bin:$PATH"

ENV APP_NAME=$APP_NAME \
  APP_PATH=$APP_PATH

# Install uv
COPY --from=ghcr.io/astral-sh/uv:python3.14-bookworm-slim /usr/local/bin/uv /usr/bin/uv


RUN groupadd --system --gid 999 ${APP_NAME} \
 && useradd --system --gid 999 --uid 999 --create-home ${APP_NAME}

# Install the project into `/app`
WORKDIR $APP_PATH

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev --no-editable --active

COPY . .

USER $APP_NAME

EXPOSE 8089

CMD ["./scripts/init-server.sh"]

### PROD


FROM python:3.14-slim AS prod

ARG VIRTUAL_ENV=/opt/venv
ARG PORT=8089
ARG APP_NAME=app
ARG APP_PATH=/app

ENV \
    VIRTUAL_ENV=$VIRTUAL_ENV \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PORT=$PORT

RUN groupadd --system --gid 999 ${APP_NAME} \
 && useradd --system --gid 999 --uid 999 --create-home ${APP_NAME}

COPY --from=base $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=base $APP_PATH $APP_PATH

WORKDIR $APP_PATH

USER $APP_NAME

CMD ["./scripts/init-server.sh"]

### DEV

FROM base AS dev

ARG PORT=8089
ENV PORT=$PORT

USER root

ENV \
  PYTHONBREAKPOINT=ipdb.set_trace

RUN uv sync --locked --no-install-project --no-editable --active

COPY . $APP_PATH

CMD ["./scripts/init-dev-server.sh"]
