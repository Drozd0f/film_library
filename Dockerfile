FROM python:3.8
EXPOSE 5000
WORKDIR film_library
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY film_library/ .
