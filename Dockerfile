FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    python-dev \
    build-essential \ 
    libmysqlclient-dev
# RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT ["python3"]
CMD ["app.py"]
