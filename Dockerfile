FROM python:3.6

WORKDIR /dash

COPY . /dash

RUN pip install --trusted-host pypi.python.org -r dash/requirements.txt

EXPOSE 8000

CMD ["python", "dash/main.py"]