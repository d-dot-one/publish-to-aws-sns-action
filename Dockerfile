FROM python:3.11.4-slim AS base

LABEL "com.github.actions.name"="Publish to AWS SNS Topic"
LABEL "com.github.actions.description"="Publish a JSON message to an AWS SNS Topic"
LABEL description="Publish a JSON message to an AWS SNS Topic"
LABEL homepage="https://github.com/d-dot-one/publish-to-sns"
LABEL maintainer="d-dot-one"
LABEL repository="https://github.com/d-dot-one/publish-to-sns"

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS python-dependencies

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends apt-utils gcc && \
    pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --deploy

FROM python-dependencies AS runtime

COPY --from=python-dependencies /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV PYTHONPATH=".:$PATH"

ARG USER_NAME="publish"
ARG GROUP_NAME="github-action"
ARG HOME_DIR="/usr/${USER_NAME}"
ENV HOME_DIR=${HOME_DIR}

RUN mkdir ${HOME_DIR} && \
    groupadd ${GROUP_NAME} &&  \
    useradd -d ${HOME_DIR} -s /bin/bash -g ${GROUP_NAME} ${USER_NAME} && \
    chown -R ${USER_NAME}:${GROUP_NAME} ${HOME_DIR}

RUN pipenv install --deploy --verbose

WORKDIR ${HOME_DIR}
USER ${USER_NAME}

COPY action/publish_to_sns.py ${HOME_DIR}
COPY action/__init__.py ${HOME_DIR}

RUN echo "#!/bin/bash\npipenv run python ${HOME_DIR}/publish_to_sns.py" > ./entrypoint.sh && \
    chmod +x ./entrypoint.sh

LABEL version="1.1.0"

ENTRYPOINT ["/bin/bash", "-c", "${HOME_DIR}/entrypoint.sh"]
