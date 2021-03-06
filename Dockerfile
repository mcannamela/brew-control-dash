FROM python:3.8.3
ENV PROJECT_DIR=/brew-control-dash
ENV PATH="${PATH}:/root/.poetry/bin"
WORKDIR $PROJECT_DIR

RUN curl --retry 5 -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml .
COPY poetry.lock .
COPY setup.py .

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

COPY . $PROJECT_DIR

RUN pip install -e .

VOLUME $PROJECT_DIR
