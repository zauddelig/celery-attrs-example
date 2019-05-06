FROM python:3.6-alpine AS base

WORKDIR /code

ADD requirements_static.txt .

RUN pip install -r requirements_static.txt

ADD . .

# run the tests
FROM base as test
RUN python setup.py test

# actual container.
FROM base as final
RUN python setup.py install
