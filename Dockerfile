# base images
FROM python:3.9

# workdir is used to set the pwd inside docker container
WORKDIR /code

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# copy whole directory inside /code working directory.
COPY . /code

# This command execute at the time when conatiner start.
CMD ["python3", "app.py"]