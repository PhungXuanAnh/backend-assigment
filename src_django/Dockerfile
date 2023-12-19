FROM python:3.9.0
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN mkdir -p /app
WORKDIR /app
COPY ./src_django/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src_django /app
EXPOSE 8000
