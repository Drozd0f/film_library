FROM python:3.8 as base
EXPOSE 5000
WORKDIR film_library
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY film_library/ .

FROM base as test
COPY requirements.test.txt .
RUN pip install -r requirements.test.txt
