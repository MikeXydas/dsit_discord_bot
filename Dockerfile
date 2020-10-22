FROM python:3.8
RUN mkdir /app
COPY ./ /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD poetry run python3 main.py 
