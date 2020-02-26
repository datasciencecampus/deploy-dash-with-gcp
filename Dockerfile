# Move to /dash

FROM python:3.6

WORKDIR /

COPY . /

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["gunicorn","--bind=0.0.0.0:8080","main:server"]